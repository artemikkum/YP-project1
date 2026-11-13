"""Тесты логики: добавление, поиск, изменение, удаление."""
import unittest

import inventory as inv


def sample(number="INV-001", **over):
    data = {"number": number, "type": "ПК", "name": "Dell 3080", "room": "101", "state": "исправно"}
    data.update(over)
    return data


class AddItemTests(unittest.TestCase):
    def test_add_ok(self):  # TC-2.1
        items = []
        item = inv.add_item(items, sample())
        self.assertEqual(len(items), 1)
        self.assertEqual(item["number"], "INV-001")

    def test_add_strips_spaces_and_lowers_state(self):  # TC-2.2
        items = []
        inv.add_item(items, sample(number="  INV-005 ", state=" Исправно "))
        self.assertEqual(items[0]["number"], "INV-005")
        self.assertEqual(items[0]["state"], "исправно")

    def test_add_empty_required_field(self):  # TC-2.3
        for field in inv.REQUIRED_FIELDS:
            with self.subTest(field=field):
                items = []
                with self.assertRaises(inv.InventoryError):
                    inv.add_item(items, sample(**{field: "   "}))
                self.assertEqual(items, [])

    def test_add_duplicate_number(self):  # TC-2.4
        items = []
        inv.add_item(items, sample())
        with self.assertRaises(inv.DuplicateError):
            inv.add_item(items, sample(number="inv-001"))  # регистр не важен
        self.assertEqual(len(items), 1)

    def test_add_bad_state(self):  # TC-2.5
        with self.assertRaises(inv.InventoryError):
            inv.add_item([], sample(state="сломано"))

    def test_add_bad_and_good_date(self):  # TC-2.6
        with self.assertRaises(inv.InventoryError):
            inv.add_item([], sample(received="01.09.2024"))
        items = []
        inv.add_item(items, sample(received="2024-09-01"))
        self.assertEqual(items[0]["received"], "2024-09-01")

    def test_optional_fields_may_be_empty(self):
        item = inv.add_item([], sample())
        self.assertEqual((item["received"], item["responsible"]), ("", ""))

    def test_unknown_fields_are_dropped(self):
        item = inv.add_item([], sample(hacker="<script>"))
        self.assertNotIn("hacker", item)


class NumberTests(unittest.TestCase):
    def test_next_number_empty(self):  # TC-2.7
        self.assertEqual(inv.next_number([]), "INV-001")

    def test_next_number_after_existing(self):
        items = [sample("INV-003"), sample("INV-010"), sample("X-77")]
        self.assertEqual(inv.next_number(items), "INV-011")

    def test_find_by_number(self):
        items = [sample("INV-001")]
        self.assertIsNotNone(inv.find_by_number(items, " inv-001 "))
        self.assertIsNone(inv.find_by_number(items, ""))
        self.assertIsNone(inv.find_by_number(items, "INV-999"))


class FormatTests(unittest.TestCase):
    def test_long_type_does_not_stick_to_next_column(self):
        item = inv.add_item([], sample(type="маршрутизатор", name="MikroTik"))
        row = inv.format_table([item]).splitlines()[-1]
        self.assertNotIn("маршрутизаторMikroTik", row)



class SearchTests(unittest.TestCase):
    def setUp(self):
        self.items = []
        inv.add_item(self.items, sample("INV-001", room="101"))
        inv.add_item(self.items, sample("INV-002", room="102", type="монитор",
                                        name="Samsung S24"))
        inv.add_item(self.items, sample("INV-003", room="101", state="списано"))

    def test_find_existing(self):  # T-07
        self.assertEqual(inv.find_by_number(self.items, "INV-002")["room"], "102")

    def test_find_missing_and_empty(self):  # T-08
        self.assertIsNone(inv.find_by_number(self.items, "INV-999"))
        self.assertIsNone(inv.find_by_number(self.items, ""))
        self.assertIsNone(inv.find_by_number(self.items, "   "))

    def test_search_by_room(self):
        found = inv.search(self.items, room="101")
        self.assertEqual([i["number"] for i in found], ["INV-001", "INV-003"])

    def test_search_by_text(self):
        found = inv.search(self.items, text="samsung")
        self.assertEqual([i["number"] for i in found], ["INV-002"])
        self.assertEqual(len(inv.search(self.items, text="МОНИТОР")), 1)

    def test_search_repeated(self):  # повторный поиск даёт тот же результат
        self.assertEqual(inv.search(self.items, room="101"),
                         inv.search(self.items, room="101"))



class UpdateDeleteTests(unittest.TestCase):
    def setUp(self):
        self.items = []
        inv.add_item(self.items, sample("INV-001"))
        inv.add_item(self.items, sample("INV-002"))

    def test_update_state_and_room(self):  # T-10
        inv.update_item(self.items, "INV-001", state="требует ремонта", room="205")
        item = inv.find_by_number(self.items, "INV-001")
        self.assertEqual(item["state"], "требует ремонта")
        self.assertEqual(item["room"], "205")

    def test_update_invalid_keeps_old_data(self):  # T-11
        with self.assertRaises(inv.InventoryError):
            inv.update_item(self.items, "INV-001", state="неизвестно")
        self.assertEqual(inv.find_by_number(self.items, "INV-001")["state"], "исправно")

    def test_update_number_forbidden(self):
        with self.assertRaises(inv.InventoryError):
            inv.update_item(self.items, "INV-001", number="INV-777")

    def test_update_missing(self):
        with self.assertRaises(inv.InventoryError):
            inv.update_item(self.items, "INV-404", room="1")

    def test_delete_ok(self):  # T-12
        inv.delete_item(self.items, "INV-001")
        self.assertEqual([i["number"] for i in self.items], ["INV-002"])

    def test_delete_missing(self):  # T-13
        with self.assertRaises(inv.InventoryError):
            inv.delete_item(self.items, "INV-404")
        self.assertEqual(len(self.items), 2)



if __name__ == "__main__":
    unittest.main()
