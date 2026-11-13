"""Первые тест-кейсы спринта 1 (TC-1.1 ... TC-1.3)."""
import os
import unittest

import inventory as inv
import storage

DATA = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "inventory.json")


class Sprint1Tests(unittest.TestCase):
    def test_demo_data_has_at_least_5_records(self):  # TC-1.1
        self.assertGreaterEqual(len(storage.load_items(DATA)), 5)

    def test_every_record_has_required_fields(self):  # TC-1.2
        for item in storage.load_items(DATA):
            for field in inv.REQUIRED_FIELDS:
                self.assertTrue(item.get(field), f"{item.get('number')}: нет поля {field}")
            self.assertIn(item["state"], inv.STATES)

    def test_table_shows_all_numbers_and_empty_list(self):  # TC-1.3
        items = storage.load_items(DATA)
        table = inv.format_table(items)
        for item in items:
            self.assertIn(item["number"], table)
        self.assertIn("записей нет", inv.format_table([]))


if __name__ == "__main__":
    unittest.main()
