import unittest

from lead_triage import normalize_lead, score_lead, triage


class LeadTriageTests(unittest.TestCase):
    def test_normalizes_email(self):
        lead = normalize_lead({"name": "Ada", "email": " ADA@EXAMPLE.COM "})
        self.assertEqual(lead["email"], "ada@example.com")

    def test_rejects_missing_email(self):
        with self.assertRaises(ValueError):
            normalize_lead({"name": "Ada"})

    def test_hot_high_intent_referral(self):
        lead = normalize_lead({
            "name": "Ada",
            "email": "ada@example.com",
            "company": "Example",
            "source": "referral",
            "budget": 1500,
            "message": "Need an automation integration and a price quote",
        })
        result = score_lead(lead)
        self.assertEqual(result["tier"], "hot")
        self.assertGreaterEqual(result["score"], 60)

    def test_triage_sorts_and_keeps_errors(self):
        result = triage([
            {"name": "Low", "email": "low@example.com"},
            {"name": "Broken"},
            {
                "name": "High",
                "email": "high@example.com",
                "company": "Acme",
                "source": "inbound",
                "budget": 2000,
                "message": "automation demo",
            },
        ])
        self.assertEqual(result["leads"][0]["email"], "high@example.com")
        self.assertEqual(len(result["errors"]), 1)


if __name__ == "__main__":
    unittest.main()
