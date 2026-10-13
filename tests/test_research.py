import unittest
from pathlib import Path

import pandas as pd

from research import build_evidence_corpus, expand_query_terms, retrieve_evidence


class EvidenceRetrievalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        data_dir = root / "data"
        cls.corpus = build_evidence_corpus(
            data_dir,
            pd.read_csv(data_dir / "gcc_directory.csv"),
            pd.read_csv(data_dir / "city_profiles.csv"),
            pd.read_csv(data_dir / "service_providers.csv"),
            pd.read_csv(data_dir / "sources.csv"),
        )

    def test_indirect_cluster_question_retrieves_report_page(self):
        matches = retrieve_evidence("Where are the main GCC hubs?", self.corpus)
        self.assertTrue(matches)
        self.assertTrue(any("Government of India report, p. 2" == item["citation"] for item in matches))
        self.assertTrue(any("Bengaluru" in item["passage"] for item in matches))

    def test_market_count_retrieves_page_level_evidence(self):
        matches = retrieve_evidence("How many capability centres are in India?", self.corpus)
        report_matches = [item for item in matches if item["kind"] == "report"]
        self.assertTrue(report_matches)
        self.assertTrue(all(item["url"].startswith("https://") for item in report_matches))

    def test_unknown_claim_does_not_match_generic_gcc_mentions(self):
        self.assertEqual(
            retrieve_evidence("What proportion of GCC teams work a four-day week?", self.corpus),
            [],
        )

    def test_indirect_office_rent_question_returns_qualified_records(self):
        matches = retrieve_evidence("What does office space cost in Chennai?", self.corpus)
        self.assertTrue(matches)
        self.assertTrue(any(item["document"] == "City profile: Chennai" for item in matches))
        city_match = next(item for item in matches if item["document"] == "City profile: Chennai")
        self.assertIn("qualitative", city_match["passage"])

    def test_synonyms_expand_indirect_queries(self):
        terms = expand_query_terms("Which hubs have skilled people?")
        self.assertIn("cluster", terms)
        self.assertIn("workforce", terms)


if __name__ == "__main__":
    unittest.main()
