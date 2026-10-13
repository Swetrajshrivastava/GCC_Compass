import math
import unittest

from location_scoring import (
    CRITERIA,
    normalize_weights,
    ordinal_score,
    rank_cities,
    rounded_weight_percentages,
)


DEFAULT_WEIGHTS = {"talent": 4, "office_cost": 3, "ecosystem": 3}


class LocationScoringTests(unittest.TestCase):
    def test_higher_talent_and_ecosystem_are_better(self):
        self.assertGreater(ordinal_score("Very high", "talent"), ordinal_score("High", "talent"))
        self.assertGreater(ordinal_score("High", "ecosystem"), ordinal_score("Medium", "ecosystem"))

    def test_high_office_cost_is_less_favorable(self):
        self.assertLess(
            ordinal_score("High", "office_cost"),
            ordinal_score("Medium", "office_cost"),
        )
        self.assertEqual(ordinal_score("Very high", "office_cost"), 1.0)
        self.assertEqual(ordinal_score("Very low", "office_cost"), 5.0)

    def test_weights_normalize_and_display_totals_100(self):
        normalized = normalize_weights({"talent": 2, "office_cost": 1, "ecosystem": 1})
        self.assertAlmostEqual(sum(normalized.values()), 1.0)
        self.assertAlmostEqual(normalized["talent"], 0.5)
        displayed = rounded_weight_percentages({"talent": 1, "office_cost": 1, "ecosystem": 1})
        self.assertEqual(sum(displayed.values()), 100)
        self.assertEqual(set(displayed), set(CRITERIA))

    def test_zero_or_invalid_weights_are_rejected(self):
        with self.assertRaises(ValueError):
            normalize_weights({"talent": 0, "office_cost": 0, "ecosystem": 0})
        with self.assertRaises(ValueError):
            normalize_weights({"talent": -1, "office_cost": 2, "ecosystem": 1})

    def test_missing_unknown_and_not_assessed_values_are_excluded(self):
        self.assertIsNone(ordinal_score("Not assessed", "talent"))
        self.assertIsNone(ordinal_score("Exceptional", "ecosystem"))
        self.assertIsNone(ordinal_score(None, "talent"))
        self.assertIsNone(ordinal_score(float("nan"), "talent"))
        rows = rank_cities(
            [{
                "city": "Partial",
                "talent_signal": "Very high",
                "office_cost_signal": "Unknown",
                "ecosystem_depth": None,
            }],
            DEFAULT_WEIGHTS,
        )
        self.assertEqual(rows[0]["assessed_criteria"], 1)
        self.assertEqual(rows[0]["evidence_completeness"], 1 / 3)
        self.assertIsNone(rows[0]["score"])
        self.assertIsNone(rows[0]["rank"])

    def test_score_renormalizes_weights_over_assessed_criteria_only(self):
        rows = rank_cities(
            [{
                "city": "Partial",
                "talent_signal": "Very high",
                "office_cost_signal": "Not assessed",
                "ecosystem_depth": None,
            }],
            DEFAULT_WEIGHTS,
            minimum_assessed=1,
        )
        self.assertEqual(rows[0]["score"], 5.0)

    def test_rank_order_excludes_insufficient_data_and_breaks_ties_by_city(self):
        records = [
            {
                "city": "Bengaluru",
                "talent_signal": "Very high",
                "office_cost_signal": "High",
                "ecosystem_depth": "High",
            },
            {
                "city": "Hyderabad",
                "talent_signal": "High",
                "office_cost_signal": "Medium-high",
                "ecosystem_depth": "High",
            },
            {
                "city": "Candidate",
                "talent_signal": "Not assessed",
                "office_cost_signal": "Not assessed",
                "ecosystem_depth": "Not assessed",
            },
        ]
        rows = rank_cities(records, DEFAULT_WEIGHTS)
        rankable = [row for row in rows if row["rank"] is not None]
        self.assertEqual([row["city"] for row in rankable], ["Bengaluru", "Hyderabad"])
        self.assertEqual([row["rank"] for row in rankable], [1, 2])
        insufficient = next(row for row in rows if row["city"] == "Candidate")
        self.assertIsNone(insufficient["rank"])
        self.assertIsNone(insufficient["score"])

    def test_score_ties_are_deterministic(self):
        records = [
            {"city": "Zulu", "talent_signal": "High", "office_cost_signal": "Medium", "ecosystem_depth": "High"},
            {"city": "Alpha", "talent_signal": "High", "office_cost_signal": "Medium", "ecosystem_depth": "High"},
        ]
        rows = rank_cities(records, DEFAULT_WEIGHTS)
        self.assertEqual([row["city"] for row in rows], ["Alpha", "Zulu"])
        self.assertTrue(math.isclose(rows[0]["score"], rows[1]["score"]))


if __name__ == "__main__":
    unittest.main()
