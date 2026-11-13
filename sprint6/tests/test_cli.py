"""Тесты консольного меню: данные хранятся в JSON-файле (спринты 4-6).

Ввод подменяется списком ответов; каждый вызов run_app работает с временным файлом,
а после завершения меню список items синхронизируется с файлом (как после перезапуска).
"""
import os
import tempfile
import unittest

import inventory as inv
import storage
from main import App

DEMO = storage.DEFAULT_PATH


def run_with_path(path, answers):
    queue = iter(answers)
    out = []

    def fake_input(prompt):
        try:
            return next(queue)
        except StopIteration:
            raise EOFError from None

    App(path, ask=fake_input, say=out.append).run()
    return "\n".join(out)


def run_app(items, answers):
    """Записывает items во временный файл, запускает меню, читает файл обратно в items."""
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "inventory.json")
        storage.save_items(items, path)
        out = run_with_path(path, answers)
        items[:] = storage.load_items(path)
    return out


def add_answers(number="INV-100", type_="ПК", name="Test PC", room="101", state="исправно", received="", resp=""):
    return ["2", number, type_, name, room, state, received, resp]


class CliTests(unittest.TestCase):
    def setUp(self):
        self.items = storage.load_items(DEMO)

    # ----- просмотр и добавление (спринт 2) -----
    def test_show_and_add(self):
        out = run_app(self.items, add_answers() + ["1", "0"])
        self.assertIn("Добавлено: INV-100", out)
        self.assertIn("Всего записей: 13", out)

    def test_duplicate_rejected(self):
        out = run_app(self.items, add_answers(number="inv-001") + ["0"])
        self.assertIn("уже существует", out)
        self.assertEqual(len(self.items), 12)

    # ----- поиск (US-4, US-5) -----
    def test_find_by_number_shows_card(self):  # TC-3.1
        out = run_app(self.items, ["3", "1", "INV-004", "0"])
        self.assertIn("Кабинет: 101", out)
        self.assertIn("требует ремонта", out)

    def test_find_by_number_not_found(self):  # TC-3.2
        out = run_app(self.items, ["3", "1", "INV-999", "0"])
        self.assertIn("Не найдено", out)

    def test_find_empty_query_does_not_crash(self):  # TC-3.3
        out = run_app(self.items, ["3", "1", "", "0"])
        self.assertIn("Пустой запрос", out)
        self.assertIn("До свидания", out)

    def test_find_by_room_lists_all_devices(self):  # TC-3.4
        out = run_app(self.items, ["3", "2", "102", "0"])
        for number in ("INV-006", "INV-007", "INV-008", "INV-009"):
            self.assertIn(number, out)
        self.assertNotIn("INV-001 ", out)

    def test_find_by_room_not_found(self):
        out = run_app(self.items, ["3", "2", "999", "0"])
        self.assertIn("Не найдено", out)

    def test_find_by_text_case_insensitive(self):
        out = run_app(self.items, ["3", "3", "SAMSUNG", "0"])
        self.assertIn("INV-003", out)
        self.assertIn("INV-004", out)

    def test_repeated_search_same_result(self):  # TC-3.5
        first = run_app(self.items, ["3", "2", "101", "0"])
        second = run_app(self.items, ["3", "2", "101", "0"])
        self.assertEqual(first, second)

    def test_bad_search_mode(self):
        out = run_app(self.items, ["3", "7", "0"])
        self.assertIn("Нужно ввести 1, 2 или 3", out)

    # ----- изменение (US-6) -----
    def test_edit_room_and_state(self):  # TC-3.6
        run_app(self.items, ["4", "INV-001", "", "", "205", "требует ремонта", "", "", "0"])
        item = inv.find_by_number(self.items, "INV-001")
        self.assertEqual((item["room"], item["state"]), ("205", "требует ремонта"))
        self.assertEqual(item["name"], "Dell OptiPlex 3080")  # Enter оставил без изменений

    def test_edit_invalid_state_keeps_old_data(self):  # TC-3.7
        out = run_app(self.items, ["4", "INV-001", "", "", "", "сломано", "", "", "0"])
        self.assertIn("Недопустимое состояние", out)
        self.assertEqual(inv.find_by_number(self.items, "INV-001")["state"], "исправно")

    def test_edit_not_found(self):
        out = run_app(self.items, ["4", "INV-999", "0"])
        self.assertIn("Не найдено", out)

    def test_edit_without_changes(self):
        out = run_app(self.items, ["4", "INV-001", "", "", "", "", "", "", "0"])
        self.assertIn("Изменений нет", out)

    # ----- удаление (US-7) -----
    def test_delete_confirmed(self):  # TC-3.8
        out = run_app(self.items, ["5", "INV-012", "да", "0"])
        self.assertIn("Запись удалена", out)
        self.assertIsNone(inv.find_by_number(self.items, "INV-012"))
        self.assertEqual(len(self.items), 11)

    def test_delete_cancelled(self):  # TC-3.9
        out = run_app(self.items, ["5", "INV-012", "нет", "0"])
        self.assertIn("Удаление отменено", out)
        self.assertEqual(len(self.items), 12)

    def test_delete_garbage_answer_cancels(self):
        run_app(self.items, ["5", "INV-012", "может быть", "0"])
        self.assertEqual(len(self.items), 12)

    def test_delete_not_found(self):  # TC-3.10
        out = run_app(self.items, ["5", "INV-999", "0"])
        self.assertIn("Не найдено", out)
        self.assertEqual(len(self.items), 12)

    # ----- устойчивость -----
    def test_not_found_everywhere(self):
        out = run_app(self.items, ["3", "1", "INV-999", "5", "INV-999", "4", "INV-999", "0"])
        self.assertEqual(out.count("Не найдено"), 3)

    def test_bad_menu_input(self):
        out = run_app(self.items, ["abc", "", "99", "0"])
        self.assertEqual(out.count("Нет такого пункта"), 3)

    def test_ctrl_d_exits_cleanly(self):
        self.assertIn("Работа завершена", run_app(self.items, ["5", "INV-001"]))
        self.assertEqual(len(self.items), 12)

    def test_full_user_scenario(self):  # TC-3.11
        out = run_app(self.items, add_answers() + ["3", "1", "INV-100", "4", "INV-100", "", "", "205", "", "", "", "5", "INV-100", "да", "0"])
        self.assertIn("Добавлено: INV-100", out)
        self.assertIn("Запись обновлена", out)
        self.assertIn("Запись удалена", out)
        self.assertEqual(len(self.items), 12)


class PersistenceTests(unittest.TestCase):
    """Сохранение между запусками (US-9, US-10)."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.path = os.path.join(self._tmp.name, "data", "inventory.json")

    def test_data_survives_restart(self):  # TC-4.1
        run_with_path(self.path, add_answers() + ["0"])
        out = run_with_path(self.path, ["3", "1", "INV-100", "0"])  # «перезапуск» и поиск
        self.assertIn("Test PC", out)

    def test_changes_survive_restart(self):  # TC-4.2
        run_with_path(self.path, add_answers() + ["0"])
        run_with_path(self.path, ["4", "INV-100", "", "", "205", "требует ремонта", "", "", "0"])
        item = storage.load_items(self.path)[0]
        self.assertEqual((item["room"], item["state"]), ("205", "требует ремонта"))
        run_with_path(self.path, ["5", "INV-100", "да", "0"])
        self.assertEqual(storage.load_items(self.path), [])

    def test_missing_file_starts_empty_and_is_created(self):  # TC-4.3
        self.assertFalse(os.path.exists(self.path))
        out = run_with_path(self.path, ["1", "0"])
        self.assertIn("записей нет", out)
        run_with_path(self.path, add_answers() + ["0"])
        self.assertTrue(os.path.exists(self.path))

    def test_corrupted_file_on_start(self):  # TC-4.4
        os.makedirs(os.path.dirname(self.path))
        with open(self.path, "w", encoding="utf-8") as f:
            f.write("[{broken")
        out = run_with_path(self.path, ["1", "0"])
        self.assertIn("повреждён", out)
        self.assertIn("записей нет", out)
        backups = [n for n in os.listdir(os.path.dirname(self.path)) if ".broken-" in n]
        self.assertEqual(len(backups), 1)  # исходные данные не потеряны

    def test_failed_add_is_not_saved(self):
        run_with_path(self.path, add_answers(room="") + ["0"])
        self.assertEqual(storage.load_items(self.path), [])

    def test_demo_data_file_is_valid(self):  # TC-4.5
        checked = []
        for item in storage.load_items(DEMO):
            inv.add_item(checked, item)
        self.assertGreaterEqual(len(checked), 10)


class FilterAndEditTests(unittest.TestCase):
    """Спринт 5: фильтр (US-8) и очистка необязательных полей."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.path = os.path.join(self._tmp.name, "inventory.json")
        storage.save_items(storage.load_items(DEMO), self.path)

    def test_filter_by_room(self):  # TC-5.5
        out = run_with_path(self.path, ["6", "101", "", "0"])
        self.assertIn("Найдено: 5", out)

    def test_filter_by_state(self):  # TC-5.6
        out = run_with_path(self.path, ["6", "", "требует ремонта", "0"])
        self.assertIn("Найдено: 2", out)
        self.assertIn("INV-004", out)
        self.assertIn("INV-007", out)

    def test_filter_by_room_and_state(self):  # TC-5.7
        out = run_with_path(self.path, ["6", "102", "исправно", "0"])
        self.assertIn("Найдено: 3", out)

    def test_filter_without_conditions_shows_all(self):
        out = run_with_path(self.path, ["6", "", "", "0"])
        self.assertIn("Найдено: 12", out)

    def test_filter_nothing_found(self):
        out = run_with_path(self.path, ["6", "999", "", "0"])
        self.assertIn("Найдено: 0", out)
        self.assertIn("записей нет", out)

    def test_filter_unknown_state(self):  # TC-5.8
        out = run_with_path(self.path, ["6", "", "сломано", "0"])
        self.assertIn("Неизвестное состояние", out)

    def test_edit_dash_clears_optional_fields(self):  # TC-5.3
        out = run_with_path(self.path, ["4", "INV-001", "", "", "", "", "-", "-", "0"])
        self.assertIn("Запись обновлена", out)
        item = inv.find_by_number(storage.load_items(self.path), "INV-001")
        self.assertEqual((item["received"], item["responsible"]), ("", ""))

    def test_edit_dash_on_required_field_is_error(self):  # TC-5.4
        out = run_with_path(self.path, ["4", "INV-001", "", "", "-", "", "", "", "0"])
        self.assertIn("обязательное", out)
        self.assertEqual(inv.find_by_number(storage.load_items(self.path), "INV-001")["room"], "101")


if __name__ == "__main__":
    unittest.main()
