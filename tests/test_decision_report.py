import unittest
from io import BytesIO

from pypdf import PdfReader

from decision_report import generate_decision_report
from location_scoring import rank_cities


class DecisionReportTests(unittest.TestCase):
    def setUp(self):
        self.city_records = [
            {
                "city": "Bengaluru",
                "talent_signal": "Very high",
                "office_cost_signal": "High",
                "ecosystem_depth": "High",
                "fit_notes": "Strong technology and product talent ecosystem",
                "policy_or_validation_note": "Validate micro-market costs",
                "source_url": "https://example.org/bengaluru?topic=city&source=profile",
            },
            {
                "city": "Chennai",
                "talent_signal": "High",
                "office_cost_signal": "Medium",
                "ecosystem_depth": "Medium-high",
                "fit_notes": "Engineering and services talent",
                "policy_or_validation_note": "Validate city-level costs",
                "source_url": "",
            },
            {
                "city": "Ahmedabad",
                "talent_signal": "Not assessed",
                "office_cost_signal": "Not assessed",
                "ecosystem_depth": "Not assessed",
                "fit_notes": "Candidate for research only",
                "policy_or_validation_note": "Assess with comparable evidence",
                "source_url": "",
            },
        ]

    def _extract(self, data):
        reader = PdfReader(BytesIO(data))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    def test_report_reflects_selected_weights_and_current_ranking(self):
        talent_weights = {"talent": 5, "office_cost": 1, "ecosystem": 1}
        cost_weights = {"talent": 1, "office_cost": 5, "ecosystem": 1}
        talent_ranking = rank_cities(self.city_records, talent_weights)
        cost_ranking = rank_cities(self.city_records, cost_weights)
        talent_report = self._extract(
            generate_decision_report(talent_ranking, talent_weights)
        )
        cost_report = self._extract(generate_decision_report(cost_ranking, cost_weights))

        self.assertIn("Talent availability", talent_report)
        self.assertIn("72%", talent_report)
        self.assertIn("Bengaluru ranks first", talent_report)
        self.assertIn("Talent availability", cost_report)
        self.assertIn("Office cost", cost_report)
        self.assertIn("72%", cost_report)
        self.assertIn("Chennai ranks first", cost_report)

    def test_report_preserves_unranked_and_missing_data_caveats(self):
        weights = {"talent": 4, "office_cost": 3, "ecosystem": 3}
        report = self._extract(
            generate_decision_report(rank_cities(self.city_records, weights), weights)
        )
        self.assertIn("Ahmedabad", report)
        self.assertIn("Unranked", report)
        self.assertIn("Insufficient data", report)
        self.assertIn("fewer than 2 of 3 criteria are assessed", report)
        self.assertIn("this is not evidence that the city is unsuitable", report)
        self.assertIn("not audited or directly comparable market benchmarks", report)

    def test_report_is_pdf_and_includes_source_url(self):
        weights = {"talent": 4, "office_cost": 3, "ecosystem": 3}
        data = generate_decision_report(rank_cities(self.city_records, weights), weights)
        text = self._extract(data)
        self.assertTrue(data.startswith(b"%PDF"))
        self.assertIn("https://example.org/bengaluru?topic=city&source=profile", text)
        self.assertIn("Strong technology and product talent ecosystem", text)
        self.assertIn("Scoring methodology and limitations", text)
        reader = PdfReader(BytesIO(data))
        linked_uris = {
            annotation.get_object()["/A"].get_object().get("/URI")
            for page in reader.pages
            for annotation in page.get("/Annots", [])
            if annotation.get_object().get("/A")
        }
        self.assertIn(
            "https://example.org/bengaluru?topic=city&source=profile",
            linked_uris,
        )


if __name__ == "__main__":
    unittest.main()
