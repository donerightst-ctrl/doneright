import tempfile
import unittest
from pathlib import Path

from app import LeadCreate, list_leads, save_lead


class LeadStoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = str(Path(self.tmp.name) / "test.sqlite3")
        self.lead = LeadCreate(
            name="Alice Example",
            email="Alice@Example.com",
            phone="+1 555 0100",
            service="Automation",
            message="Please automate our intake form.",
        )

    def tearDown(self):
        self.tmp.cleanup()

    def test_save_and_list(self):
        lead_id, duplicate = save_lead(self.lead, self.db)
        self.assertFalse(duplicate)
        rows = list_leads(db_path=self.db)
        self.assertEqual(rows[0]["id"], lead_id)
        self.assertEqual(rows[0]["email"], "alice@example.com")
        self.assertEqual(rows[0]["service"], "Automation")

    def test_exact_business_duplicate_is_idempotent(self):
        first_id, first_dup = save_lead(self.lead, self.db)
        second_id, second_dup = save_lead(self.lead, self.db)
        self.assertFalse(first_dup)
        self.assertTrue(second_dup)
        self.assertEqual(first_id, second_id)
        self.assertEqual(len(list_leads(db_path=self.db)), 1)

    def test_different_message_creates_new_lead(self):
        first_id, _ = save_lead(self.lead, self.db)
        changed = self.lead.model_copy(update={"message": "A different request"})
        second_id, second_dup = save_lead(changed, self.db)
        self.assertFalse(second_dup)
        self.assertNotEqual(first_id, second_id)
        self.assertEqual(len(list_leads(db_path=self.db)), 2)


if __name__ == "__main__":
    unittest.main()
