"""Тесты файлового хранения storage.py."""
import json
import os
import tempfile
import unittest

import storage


class StorageTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.path = os.path.join(self._tmp.name, "data", "inventory.json")

    def test_missing_file_gives_empty_list(self):  # T-14
        self.assertEqual(storage.load_items(self.path), [])

    def test_save_and_load_roundtrip(self):  # T-15
        items = [{"number": "INV-001", "name": "Монитор «Samsung»", "room": "101"}]
        storage.save_items(items, self.path)  # папка data создаётся сама
        self.assertEqual(storage.load_items(self.path), items)

    def test_unicode_is_readable_in_file(self):
        storage.save_items([{"name": "Принтер"}], self.path)
        with open(self.path, encoding="utf-8") as f:
            self.assertIn("Принтер", f.read())

    def test_empty_file(self):  # T-16
        os.makedirs(os.path.dirname(self.path))
        open(self.path, "w").close()
        self.assertEqual(storage.load_items(self.path), [])

    def test_corrupted_json_is_backed_up(self):  # T-17
        os.makedirs(os.path.dirname(self.path))
        with open(self.path, "w", encoding="utf-8") as f:
            f.write("{ это не json")
        with self.assertRaises(storage.CorruptedStorageError) as ctx:
            storage.load_items(self.path)
        backup = ctx.exception.backup_path
        self.assertTrue(os.path.exists(backup))      # данные не потеряны
        self.assertFalse(os.path.exists(self.path))  # старый файл убран с дороги
        with open(backup, encoding="utf-8") as f:
            self.assertEqual(f.read(), "{ это не json")

    def test_wrong_structure_is_corrupted(self):
        os.makedirs(os.path.dirname(self.path))
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump({"a": 1}, f)
        with self.assertRaises(storage.CorruptedStorageError):
            storage.load_items(self.path)

    def test_save_leaves_no_tmp_file(self):
        storage.save_items([], self.path)
        self.assertFalse(os.path.exists(self.path + ".tmp"))


if __name__ == "__main__":
    unittest.main()
