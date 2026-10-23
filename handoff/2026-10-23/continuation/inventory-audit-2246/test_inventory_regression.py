#!/usr/bin/env python3
"""Offline tests: selector behavior and frozen public evidence consistency.
The report was produced by the authoritative committed guard on frozen bytes.
These tests do not purport to rerun the guard without its repository/assets.
"""
import copy
import json
from pathlib import Path
import sys
import unittest
sys.dont_write_bytecode = True
from audit_icml_inventory import BASELINE_SHA256, COMMIT, select_venue, incomplete, collisions, source_identity

HERE = Path(__file__).resolve().parent
REPORT = json.loads((HERE / 'inventory_report.public.json').read_text())

class SelectorRegression(unittest.TestCase):
    def test_case_insensitive_venue(self):
        rows = [{'id': 'X1', 'venue': v} for v in ('ICML', 'icml', 'IcMl')]
        for v in ('ICML', 'icml', 'IcMl'):
            self.assertEqual(select_venue(rows, v), rows)

    def test_venue_not_id_prefix(self):
        rows = [{'id': 'unrelated-publisher-token', 'venue': 'ICML'},
                {'id': 'icml2020-false-positive', 'venue': 'NeurIPS'},
                {'id': 'ICML2020-no-venue'}, {'id': 'icml-venue-list', 'venue': ['ICML']}]
        self.assertEqual(select_venue(rows), rows[:1])

    def test_exact_venue_not_substring_or_whitespace_alias(self):
        rows = [{'id': str(i), 'venue': v} for i, v in enumerate(('ICML', 'NotICML', 'ICML Workshop', ' ICML ', None))]
        self.assertEqual(select_venue(rows), rows[:1])

    def test_all_years_tracks_and_unknown_publication_types(self):
        rows = [{'id': 'a', 'venue': 'icml', 'year': 2018, 'track': 'Workshop', 'publication_type': None},
                {'id': 'b', 'venue': 'ICML', 'year': 2029, 'track': 'Main', 'publication_type': 'short_paper'}]
        self.assertEqual(select_venue(rows), rows)

    def test_false_is_not_missing_zero_or_null(self):
        rows = [{'id': str(i), 'metadata_ready': flag} for i, flag in enumerate((False, True, None, 0, '', 'false'))]
        rows.append({'id': 'missing'})
        self.assertEqual(incomplete(rows), rows[:1])

    def test_preserve_case_sensitive_ids_source_ids_and_duplicate_rows(self):
        rows = [{'id': 'ICML2020-case', 'venue': 'icml', 'publisher_id': 'PubID'},
                {'id': 'icml2020-case', 'venue': 'ICML', 'publisher_id': 'pubid'}]
        before = copy.deepcopy(rows)
        result = select_venue(rows)
        self.assertEqual(result, before)
        self.assertEqual(rows, before)
        self.assertIs(result[0], rows[0])
        self.assertEqual([p['id'] for p in result], ['ICML2020-case', 'icml2020-case'])
        self.assertEqual(len(select_venue(rows + [rows[0]])), 3)

    def test_collision_report_never_merges(self):
        rows = [{'id': 'ICML2020-case', 'venue': 'ICML'}, {'id': 'icml2020-case', 'venue': 'icml'}]
        found = collisions(rows, lambda p: p['id'], str.casefold)
        self.assertEqual(len(found), 1)
        self.assertFalse(found[0]['merged'])
        self.assertEqual([p['id'] for p in found[0]['records']], [p['id'] for p in rows])
        self.assertEqual(len(select_venue(rows)), 2)

    def test_source_identity_is_not_catalogue_identity(self):
        row = {'id': 'icml2020-337', 'venue': 'ICML', 'publisher_id': 'SeparateStoredID',
               'url': 'https://proceedings.mlr.press/v119/golany20a.html'}
        before = copy.deepcopy(row)
        found = source_identity(row)
        self.assertEqual(found['pmlr_url_identities'][0]['publisher_paper_id'], 'golany20a')
        self.assertEqual(found['stored_source_ids']['publisher_id'], 'SeparateStoredID')
        self.assertFalse(found['id_rewritten'])
        self.assertEqual(row, before)

class FrozenEvidenceRegression(unittest.TestCase):
    def test_exact_baseline_binding(self):
        self.assertEqual(REPORT['baseline']['source_commit'], COMMIT)
        self.assertEqual(REPORT['baseline']['papers_sha256'], BASELINE_SHA256)
        self.assertEqual(REPORT['baseline']['catalogue_records'], 2008)
        self.assertEqual(REPORT['counts']['all_icml']['records'], 403)

    def test_all_years_and_42_incomplete(self):
        count = REPORT['counts']['metadata_incomplete']
        self.assertEqual(count['records'], 42)
        self.assertEqual(count['by_year'], {'2020': 16, '2021': 7, '2022': 2, '2023': 1, '2024': 7, '2025': 8, '2026': 1})
        self.assertEqual(count['by_track'], {'Main': 42})
        self.assertEqual(count['by_publication_type'], {'None': 4, 'full_paper': 38})
        self.assertEqual(len(incomplete(select_venue(REPORT['all_icml_flag_guard_matrix'], 'icML'))), 42)

    def test_absence_is_separate_from_clearance(self):
        counts = REPORT['counts']
        self.assertEqual(counts['records_with_absent_asset_path_or_file'], 27)
        self.assertEqual(counts['records_with_both_files_present_but_uncleared'], 15)
        self.assertEqual(counts['incomplete_asset_physical_states'], {'path_absent': 53, 'local_file_present': 31,
                         'referenced_local_file_absent': 0, 'nonlocal_or_invalid_reference': 0})
        self.assertEqual(counts['incomplete_present_but_held_assets'], 26)
        self.assertEqual(counts['incomplete_cleared_assets'], 5)
        self.assertEqual(counts['clearance_pair_states'], {'both_hold': 37, 'one_cleared_one_hold': 5})

    def test_langbein_mixed_absent_cleared(self):
        row = next(p for p in REPORT['incomplete_records'] if p['id'] == 'icml2025-74254eccfd9d')
        self.assertEqual(row['assets']['first_page']['physical_state'], 'path_absent')
        self.assertEqual(row['assets']['main_figure']['source_guard']['status'], 'cleared')
        self.assertEqual(row['source_identity']['pmlr_url_identities'][0]['publisher_paper_id'], 'langbein25a')

    def test_three_uppercase_ids_retained_without_new_scope_claim(self):
        expected = {'ICML2020-chen20h', 'ICML2020-brennan20a', 'ICML2020-bao20b'}
        self.assertEqual(set(REPORT['identity_audit']['lowercase_prefix_scan_would_miss_incomplete_ids']), expected)
        rows = [p for p in REPORT['incomplete_records'] if p['id'] in expected]
        self.assertEqual(len(rows), 3)
        for row in rows:
            self.assertEqual(row['medical_scope_decision'], 'include')
            self.assertFalse(row['new_scope_adjudication'])
            self.assertEqual(row['prior_packet_annotations'][0]['category'], 'unscreened_in_current_packet')

    def test_26_record_packet_is_not_all_42(self):
        old = REPORT['narrow_packet_reconciliation']
        self.assertEqual(old['baseline_records'], 26)
        self.assertEqual(old['group_counts'], {'component_rights_hold': 5, 'source_access_hold': 6,
                         'scope_hold_or_proposal': 10, 'unscreened_in_current_packet': 3, 'selected_review_pending_at_baseline': 2})
        self.assertEqual(len(old['icml_incomplete_outside_narrow_packet']), 16)
        self.assertEqual(old['unaccounted_for_ids'], [])
        self.assertEqual(old['out_of_scope_annotated_ids'], [])
        self.assertEqual(old['overlapping_annotations'], [])
        self.assertEqual(len(old['other_venue_candidates_excluded_from_icml_counts']), 2)

    def test_guard_is_independent_and_no_mismatch(self):
        self.assertEqual(REPORT['guard_consistency']['metadata_flag_vs_source_guard_mismatches'], [])
        self.assertEqual(REPORT['guard_consistency']['cached_media_vs_source_guard_mismatches'], [])
        self.assertEqual(len(REPORT['all_icml_flag_guard_matrix']), 403)
        for row in REPORT['all_icml_flag_guard_matrix']:
            self.assertIs(row['metadata_ready'], row['source_guard_core_ready'])

    def test_source_and_id_collisions_reported_not_merged(self):
        checks = REPORT['identity_audit']['collision_checks']
        self.assertEqual(set(checks), {'exact_catalogue_id_global', 'casefold_catalogue_id_global',
            'normalized_title_global_touching_icml', 'exact_article_url_global_touching_icml',
            'exact_pdf_url_global_touching_icml', 'pmlr_source_identity_collisions'})
        self.assertTrue(all(not v for v in checks.values()))
        self.assertFalse(REPORT['selection']['ids_rewritten_or_merged'])
        self.assertEqual(REPORT['identity_audit']['source_id_url_variants'], [])

    def test_current_40_observation_separate_from_baseline_42(self):
        current = REPORT['later_current_observation']
        self.assertEqual(current['papers_sha256_after_audit'], '8ad448e88dee4620d832457bf7d9f6a80663ea98c2880ffae04c979c7b1a10e0')
        self.assertEqual(current['metadata_counts_only_not_mixed_with_baseline_guard']['records'], 40)
        self.assertEqual({p['id'] for p in current['changes_to_icml_records_from_baseline']},
                         {'icml2020-laforgue20a', 'icml2020-wang20w'})
        self.assertTrue(current['changed_since_baseline'])
        self.assertFalse(current['audit_made_active_writes'])
        self.assertEqual(REPORT['counts']['metadata_incomplete']['records'], 42)

    def test_no_new_credit_no_exhaustion_no_deployed_fix(self):
        c = REPORT['credit_and_limits']
        self.assertEqual(c['new_paper_credit'], 0)
        self.assertEqual(c['new_scientific_reading_credit'], 0)
        self.assertEqual(c['new_core_completion_credit'], 0)
        self.assertFalse(c['venue_exhaustion_claimed'])
        self.assertFalse(c['all_indexed_scope_reapproved'])
        self.assertEqual(REPORT['browser_filter_observation']['existing_expression'], '(!venue||p.venue===venue)')

    def test_report_sanitized(self):
        text = (HERE / 'inventory_report.public.json').read_text()
        for forbidden in ('/workspace/', '/home/agent/', '/tmp/', 'file://'):
            self.assertNotIn(forbidden, text)
        for row in REPORT['incomplete_records']:
            for key in ('venue', 'year', 'track', 'publication_type', 'source_identity'):
                self.assertIn(key, row)

if __name__ == '__main__':
    unittest.main(verbosity=2)
