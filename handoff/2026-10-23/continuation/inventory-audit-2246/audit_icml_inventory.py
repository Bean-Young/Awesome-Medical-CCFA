#!/usr/bin/env python3
"""Read-only, commit-bound venue inventory. Writes only to an external output directory.

Use --root REPO --output EXTERNAL_DIR --holds INPUT_JSON. The default commit and
expected digest identify v325. Source IDs, scope, metadata, rights and credits are
never changed. private_baseline is a reproducibility fixture, not a public file.
"""
import argparse
import base64
import collections
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import urlparse

sys.dont_write_bytecode = True
COMMIT = 'f4e40dfdae8b946111ce8547447115d7afdba956'
BASELINE_SHA256 = '1a89c684bf8d16da15b8e4c43edde14dcdf089c623d377335bedb976aa9f19a5'
KINDS = ('first_page', 'main_figure')


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def select_venue(records, venue='ICML'):
    """Case-insensitive venue equality only; never select, rename or dedupe by ID."""
    if not isinstance(venue, str):
        raise TypeError('venue must be a string')
    return [p for p in records if isinstance(p.get('venue'), str)
            and p['venue'].casefold() == venue.casefold()]


def incomplete(records):
    """Exactly metadata_ready=false. Missing or malformed flags are separate."""
    return [p for p in records if p.get('metadata_ready') is False]


def collisions(records, key, transform=lambda x: x):
    groups = collections.defaultdict(list)
    for p in records:
        value = key(p)
        if isinstance(value, str) and value:
            groups[transform(value)].append({'id': p['id'], 'venue': p.get('venue'), 'value': value})
    return [{'comparison_key': k, 'records': v, 'merged': False}
            for k, v in sorted(groups.items()) if len(v) > 1]


def source_identity(p):
    """Keep literal source URL/IDs, derive a separate PMLR identity, never rewrite ID."""
    ids = {k: p[k] for k in ('catalogue_id', 'publisher_id', 'official_id',
                            'official_paper_id', 'paper_id', 'source_id') if k in p}
    derived = []
    for key in ('url', 'pdf_url'):
        raw = p.get(key)
        if not isinstance(raw, str):
            continue
        parsed = urlparse(raw)
        match = None
        if parsed.hostname == 'proceedings.mlr.press':
            match = re.match(r'^/(v\d+)/([^/]+?)(?:\.html|/[^/]+\.pdf)$', parsed.path)
        elif parsed.hostname == 'raw.githubusercontent.com':
            match = re.match(r'^/mlresearch/(v\d+)/main/assets/([^/]+)/[^/]+\.pdf$', parsed.path)
        if match:
            derived.append({'source_field': key, 'volume': match[1],
                            'publisher_paper_id': match[2], 'literal_source_url': raw})
    return {'stored_source_ids': ids, 'pmlr_url_identities': derived,
            'id_rewritten': False, 'identity_note': 'Derived URL identity is not a replacement catalogue ID.'}


def freeze_baseline(root, output, commit, expected_sha):
    """Reconstruct exact committed bytes, copy only committed asset references."""
    git = lambda path: subprocess.check_output(['git', '-C', str(root), 'show', f'{commit}:{path}'])
    manifest = json.loads(git('data/catalogue-source/manifest.json'))
    recipe = manifest['outputs']['data/snapshot.json']
    assert recipe['kind'] == 'chunks'
    parts = []
    for entry in recipe['chunks']:
        raw = git('data/catalogue-source/chunks/' + entry['sha256'] + '.part')
        assert len(raw) == entry['bytes'] and sha256(raw) == entry['sha256']
        parts.append(raw)
    snapshot = b''.join(parts)
    assert sha256(snapshot) == recipe['sha256']
    recipe = manifest['outputs']['data/papers.json']
    assert recipe['kind'] == 'slice'
    raw = (base64.b64decode(recipe['prefix_b64'])
           + snapshot[recipe['start']:recipe['start'] + recipe['length']]
           + base64.b64decode(recipe['suffix_b64']))
    assert sha256(raw) == recipe['sha256'] == expected_sha
    frozen = output / 'private_baseline'
    (frozen / 'data').mkdir(parents=True, exist_ok=True)
    (frozen / 'scripts').mkdir(exist_ok=True)
    (frozen / 'data/papers.json').write_bytes(raw)
    guard = git('scripts/media_rights.py')
    (frozen / 'scripts/media_rights.py').write_bytes(guard)
    papers = json.loads(raw)
    spec = importlib.util.spec_from_file_location('frozen_readonly_media_rights', frozen / 'scripts/media_rights.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    tree = subprocess.check_output(['git', '-C', str(root), 'ls-tree', '-r', '-z', commit, 'assets'])
    blobs = {}
    for item in tree.split(b'\0'):
        if item:
            info, name = item.split(b'\t', 1)
            blobs[name.decode()] = info.split()[2].decode()
    asset_manifest = []
    for path in sorted({module.asset(p.get(k)) for p in select_venue(papers) for k in KINDS} - {''}):
        if not path.startswith('assets/') or '..' in Path(path).parts:
            continue
        if path not in blobs:
            asset_manifest.append({'asset_path': path, 'committed_file_present': False})
            continue
        candidate = root / path
        data = candidate.read_bytes() if candidate.is_file() and not candidate.is_symlink() else b''
        obj = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        if obj != blobs[path]:
            data = git(path)
            obj = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert obj == blobs[path]
        target = frozen / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        asset_manifest.append({'asset_path': path, 'committed_file_present': True,
                               'git_blob': obj, 'sha256': sha256(data), 'bytes': len(data)})
    return frozen, papers, module, asset_manifest, sha256(guard)


def counts(rows):
    def c(field):
        return dict(sorted(collections.Counter(str(r.get(field)) for r in rows).items()))
    return {'records': len(rows), 'by_year': c('year'), 'by_track': c('track'),
            'by_publication_type': c('publication_type'), 'by_venue_literal': c('venue')}


def audit(root, output, holds_path, commit=COMMIT, expected_sha=BASELINE_SHA256):
    root, output = root.resolve(), output.resolve()
    if output == root or output.is_relative_to(root):
        raise ValueError('Output must be outside the active repository')
    output.mkdir(parents=True, exist_ok=True)
    current_before = (root / 'data/papers.json').read_bytes()
    frozen, papers, guard, asset_manifest, guard_hash = freeze_baseline(root, output, commit, expected_sha)
    selected = select_venue(papers)
    hold_bytes = holds_path.read_bytes()
    holds = json.loads(hold_bytes)
    hold_groups = {
        'component_rights_hold': holds['component_permission_uncertainties'],
        'source_access_hold': holds['source_access_unavailable'],
        'scope_hold_or_proposal': holds['separate_scope_holds_or_proposals'],
        'unscreened_in_current_packet': holds['additional_unscreened_candidates'],
        'selected_review_pending_at_baseline': [{'id': x} for x in holds['selected_for_exact_two_profile_review']],
    }
    hold_annotations = collections.defaultdict(list)
    for category, records in hold_groups.items():
        for row in records:
            hold_annotations[row['id']].append({'category': category, 'status': row.get('status'),
                'source_url': row.get('source_url'),
                'finding': row.get('finding') or row.get('reason'),
                'origin': 'Narrow ICML 2020–2023 packet; not a new scope or rights decision.'})
    details = []
    cached_mismatches, flag_mismatches = [], []
    for p in selected:
        rights = {k: guard.decide(p, k, frozen) for k in KINDS}
        guard_ready = guard.core(p, rights)
        if p.get('metadata_ready') is not guard_ready:
            flag_mismatches.append({'id': p['id'], 'metadata_ready': p.get('metadata_ready'), 'source_guard_core_ready': guard_ready})
        assets = {}
        for kind, decision in rights.items():
            path = guard.asset(p.get(kind))
            safe = bool(path and path.startswith('assets/') and '..' not in Path(path).parts)
            file_exists = bool(safe and (frozen / path).is_file())
            physical = 'path_absent' if not path else ('local_file_present' if file_exists else
                        'referenced_local_file_absent' if safe else 'nonlocal_or_invalid_reference')
            cached = p.get('media_display_permissions', {}).get(kind, {})
            compare = ('status', 'reason', 'asset_path', 'asset_sha256')
            matches = all(cached.get(k) == decision.get(k) for k in compare)
            if not matches:
                cached_mismatches.append({'id': p['id'], 'asset_kind': kind})
            assets[kind] = {'path': path, 'physical_state': physical,
                'source_guard': {k: decision[k] for k in compare if k in decision},
                'cached_display_status': cached.get('status'),
                'cached_display_reason': cached.get('reason'), 'cached_matches_source_guard': matches}
        present = sum(a['physical_state'] == 'local_file_present' for a in assets.values())
        cleared = sum(a['source_guard']['status'] == 'cleared' for a in assets.values())
        details.append({'id': p['id'], 'title': p['title'], 'venue': p.get('venue'),
            'year': p.get('year'), 'track': p.get('track'), 'publication_type': p.get('publication_type'),
            'publication_type_field_present': 'publication_type' in p,
            'paper_type': p.get('paper_type'), 'publication_status': p.get('publication_status'),
            'url': p.get('url'), 'pdf_url': p.get('pdf_url'), 'source_identity': source_identity(p),
            'metadata_ready': p.get('metadata_ready'), 'source_guard_core_ready': guard_ready,
            'core_readiness_matches_flag': p.get('metadata_ready') is guard_ready,
            'catalogue_eligible': p.get('catalogue_eligible'), 'eligible_ccf_a': p.get('eligible_ccf_a'),
            'medical_scope_decision': p.get('medical_scope_decision'),
            'physical_pair_state': {0: 'both_absent', 1: 'one_absent_one_present', 2: 'both_present'}[present],
            'clearance_pair_state': {0: 'both_hold', 1: 'one_cleared_one_hold', 2: 'both_cleared'}[cleared],
            'metadata_blockers': p.get('metadata_blockers'), 'assets': assets,
            'prior_packet_annotations': hold_annotations.get(p['id'], []),
            'new_scope_adjudication': False, 'new_rights_adjudication': False})
    pending = incomplete(details)
    older = [p for p in pending if p['year'] in (2020, 2021, 2022, 2023)
             and p.get('medical_scope_decision') == 'include' and p.get('catalogue_eligible')]
    old_ids = {p['id'] for p in older}
    missing_records = [p for p in pending if p['physical_pair_state'] != 'both_present']
    present_uncleared = [p for p in pending if p['physical_pair_state'] == 'both_present'
                        and p['clearance_pair_state'] != 'both_cleared']
    all_asset_states = collections.Counter(a['physical_state'] for p in pending for a in p['assets'].values())
    for key in ('path_absent', 'referenced_local_file_absent', 'local_file_present', 'nonlocal_or_invalid_reference'):
        all_asset_states.setdefault(key, 0)
    reasons = collections.Counter(a['source_guard']['reason'] for p in pending for a in p['assets'].values())
    all_scope = {p['id'] for p in selected}
    normalize_title = lambda x: re.sub(r'\W+', '', x.casefold())
    collision_checks = {
        'exact_catalogue_id_global': collisions(papers, lambda p: p.get('id')),
        'casefold_catalogue_id_global': collisions(papers, lambda p: p.get('id'), str.casefold),
        'normalized_title_global_touching_icml': [x for x in collisions(papers, lambda p: p.get('title'), normalize_title)
                                                if any(r['id'] in all_scope for r in x['records'])],
        'exact_article_url_global_touching_icml': [x for x in collisions(papers, lambda p: p.get('url'))
                                                if any(r['id'] in all_scope for r in x['records'])],
        'exact_pdf_url_global_touching_icml': [x for x in collisions(papers, lambda p: p.get('pdf_url'))
                                            if any(r['id'] in all_scope for r in x['records'])],
    }
    source_groups = collections.defaultdict(list)
    source_variants = []
    for p in selected:
        identity = source_identity(p)
        keys = {(x['volume'], x['publisher_paper_id']) for x in identity['pmlr_url_identities']}
        for k in keys:
            source_groups[k].append(p['id'])
        if len(keys) > 1:
            source_variants.append({'id': p['id'], 'identities': identity['pmlr_url_identities'], 'merged': False})
    collision_checks['pmlr_source_identity_collisions'] = [
        {'volume': k[0], 'publisher_paper_id': k[1], 'catalogue_ids': ids, 'merged': False}
        for k, ids in sorted(source_groups.items()) if len(ids) > 1]
    current_after = (root / 'data/papers.json').read_bytes()
    current_commit = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD']).decode().strip()
    current_manifest = json.loads(subprocess.check_output(['git', '-C', str(root), 'show', current_commit + ':data/catalogue-source/manifest.json']))
    current_saved = current_manifest['outputs']['data/papers.json']['sha256'] == sha256(current_after)
    later = json.loads(current_after)
    later_selected = select_venue(later)
    current_changes = []
    baseline_by_id = {p['id']: p for p in papers}
    for p in later:
        previous = baseline_by_id.get(p['id'])
        if previous != p and (p.get('venue') == 'ICML' or previous and previous.get('venue') == 'ICML'):
            current_changes.append({'id': p['id'], 'metadata_ready_baseline': previous.get('metadata_ready') if previous else None,
                                    'metadata_ready_later': p.get('metadata_ready'),
                                    'changed_fields': sorted(k for k in set(p) | set(previous or {}) if p.get(k) != (previous or {}).get(k))})
    report = {'report_type': 'Read-only frozen ICML metadata and media inventory; no new scientific or rights decisions',
        'baseline': {'label': 'v325', 'source_commit': commit, 'papers_sha256': expected_sha,
            'guard_source': 'scripts/media_rights.py', 'guard_sha256': guard_hash,
            'guard_execution': 'Imported exact committed source with sys.dont_write_bytecode=True; no network.',
            'assets': 'Only exact committed asset blobs copied and hash-verified in a separate fixture.',
            'catalogue_records': len(papers)},
        'selection': {'criterion': 'venue is a string and venue.casefold() == ICML.casefold(); metadata_ready is False',
            'all_years_included': True, 'all_tracks_included': True, 'id_prefix_used': False,
            'ids_rewritten_or_merged': False, 'missing_publication_type_not_inferred': True},
        'counts': {'all_icml': counts(selected), 'metadata_incomplete': counts(pending),
            'metadata_ready_true': len([p for p in selected if p.get('metadata_ready') is True]),
            'missing_or_nonboolean_metadata_flag': len([p for p in selected if type(p.get('metadata_ready')) is not bool]),
            'records_with_absent_asset_path_or_file': len(missing_records),
            'records_with_both_files_present_but_uncleared': len(present_uncleared),
            'physical_pair_states': dict(collections.Counter(p['physical_pair_state'] for p in pending)),
            'clearance_pair_states': dict(collections.Counter(p['clearance_pair_state'] for p in pending)),
            'incomplete_asset_physical_states': dict(all_asset_states),
            'incomplete_asset_guard_reasons': dict(reasons),
            'incomplete_cleared_assets': sum(a['source_guard']['status'] == 'cleared' for p in pending for a in p['assets'].values()),
            'incomplete_present_but_held_assets': sum(a['physical_state'] == 'local_file_present' and a['source_guard']['status'] != 'cleared' for p in pending for a in p['assets'].values())},
        'guard_consistency': {'scope': 'All 403 ICML records, not only incomplete rows',
            'metadata_flag_vs_source_guard_mismatches': flag_mismatches,
            'cached_media_vs_source_guard_mismatches': cached_mismatches,
            'metadata_flag_is_not_used_as_asset_or_permission_evidence': True},
        'narrow_packet_reconciliation': {'source_file_label': 'remaining_candidate_inventory.json',
            'source_sha256': sha256(hold_bytes), 'scope': 'Existing eligible, indexed-included ICML 2020–2023 rows with uncleared assets; NOT all ICML incomplete records.',
            'baseline_records': len(older), 'group_counts': {k: len(v) for k, v in hold_groups.items()},
            'group_ids': {k: [p['id'] for p in v] for k, v in hold_groups.items()},
            'unaccounted_for_ids': sorted(old_ids - set(hold_annotations)),
            'out_of_scope_annotated_ids': sorted(set(hold_annotations) - old_ids),
            'overlapping_annotations': [k for k, v in hold_annotations.items() if len(v) > 1],
            'icml_incomplete_outside_narrow_packet': [p['id'] for p in pending if p['id'] not in old_ids],
            'other_venue_candidates_excluded_from_icml_counts': [p['id'] for p in holds['distinct_existing_neurips_candidates_license_pending']]},
        'identity_audit': {'canonical_ids_preserved': True,
            'uppercase_icml_prefix_ids': [p['id'] for p in selected if p['id'].startswith('ICML')],
            'lowercase_prefix_scan_would_miss_incomplete_ids': [p['id'] for p in pending if not p['id'].startswith('icml')],
            'source_id_url_variants': source_variants, 'collision_checks': collision_checks,
            'collision_policy': 'Report candidate collisions and variants; never merge or rewrite.'},
        'browser_filter_observation': {'source_file': 'app.js',
            'existing_expression': '(!venue||p.venue===venue)',
            'current_data_has_only_canonical_ICML_venue_literal': all(p['venue'] == 'ICML' for p in selected),
            'browser_filter_is_exact_match_not_id_prefix': True,
            'staged_regression_scope': 'Inventory selector only. No deployed browser filter change or browser test claimed.'},
        'later_current_observation': {'source_commit': current_commit,
            'papers_match_saved_source_commit': current_saved,
            'saved_version_label': 'v326' if current_commit == 'f7d117696cf28ee40781f269d2df989660ddf314' and current_saved else None,
            'papers_sha256_before_audit': sha256(current_before),
            'papers_sha256_after_audit': sha256(current_after),
            'changed_since_baseline': sha256(current_after) != expected_sha,
            'changed_during_this_frozen_audit': current_before != current_after,
            'metadata_counts_only_not_mixed_with_baseline_guard': counts(incomplete(later_selected)),
            'changes_to_icml_records_from_baseline': current_changes,
            'audit_made_active_writes': False},
        'credit_and_limits': {'new_paper_credit': 0, 'new_scientific_reading_credit': 0,
            'new_core_completion_credit': 0, 'active_source_changed_by_audit': False,
            'venue_exhaustion_claimed': False, 'all_indexed_scope_reapproved': False,
            'publication_type_missing_is_not_a_new_scientific_exclusion': True},
        'incomplete_records': pending,
        'all_icml_flag_guard_matrix': [{'id': p['id'], 'venue': p['venue'], 'year': p['year'], 'track': p['track'],
            'publication_type': p['publication_type'], 'metadata_ready': p['metadata_ready'],
            'source_guard_core_ready': p['source_guard_core_ready']} for p in details]}
    serialized = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
    for private_prefix in ('/workspace/', '/home/agent/', '/tmp/', 'file://'):
        assert private_prefix not in serialized, 'Private path leaked into public report'
    (output / 'inventory_report.public.json').write_text(serialized)
    (output / 'baseline_asset_manifest.json').write_text(json.dumps(asset_manifest, indent=2) + '\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--holds', type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.root, args.output, args.holds)
    print(json.dumps(result['counts'], indent=2))
