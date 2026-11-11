"""Тесты консольного меню спринта 3: ввод подменяется списком ответов, данные в памяти."""
import unittest

import inventory as inv
from main import App, DATA_FILE


def run_app(items, answers):
    queue = iter(answers)
    out = []

    def fake_input(prompt):
        try:
            return next(queue)
        except StopIteration:
            raise EOFError from None

    App(items, ask=fake_input, say=out.append).run()
    return "\n".join(out)


def add_answers(number="INV-100", type_="ПК", name="Test PC", room="101", state="исправно", received="", resp=""):
    return ["2", number, type_, name, room, state, received, resp]


class CliTests(unittest.TestCase):
    def setUp(self):
        self.items = inv.load_demo(DATA_FILE)

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


if __name__ == "__main__":
    unittest.main()
