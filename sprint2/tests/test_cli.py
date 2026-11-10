"""Тесты консольного меню: ввод подменяется списком ответов."""
import os
import unittest

import inventory as inv
from main import App, DATA_FILE


def run_app(items, answers):
    """Запускает меню с готовыми ответами; возвращает вывод одной строкой."""
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

    def test_show_lists_all_items(self):  # TC-2.8
        out = run_app(self.items, ["1", "0"])
        self.assertIn("INV-012", out)
        self.assertIn("Всего записей: 12", out)

    def test_show_empty(self):
        out = run_app([], ["1", "0"])
        self.assertIn("записей нет", out)
        self.assertIn("Всего записей: 0", out)

    def test_add_ok_then_visible(self):  # TC-2.9
        out = run_app(self.items, add_answers() + ["1", "0"])
        self.assertIn("Добавлено: INV-100", out)
        self.assertIn("Всего записей: 13", out)
        self.assertEqual(len(self.items), 13)

    def test_add_auto_number(self):  # TC-2.10
        out = run_app(self.items, add_answers(number="") + add_answers(number="") + ["0"])
        self.assertIn("Присвоен номер: INV-013", out)
        self.assertIn("Присвоен номер: INV-014", out)

    def test_duplicate_rejected(self):  # TC-2.11
        out = run_app(self.items, add_answers(number="inv-001") + ["0"])
        self.assertIn("уже существует", out)
        self.assertEqual(len(self.items), 12)

    def test_empty_required_field_rejected(self):  # TC-2.12
        out = run_app(self.items, add_answers(room="") + ["0"])
        self.assertIn("Кабинет", out)
        self.assertIn("Запись не добавлена", out)
        self.assertEqual(len(self.items), 12)

    def test_bad_state_and_date_rejected(self):  # TC-2.12
        out = run_app(self.items, add_answers(state="сломано") + add_answers(received="01.09.2024") + ["0"])
        self.assertIn("Недопустимое состояние", out)
        self.assertIn("ГГГГ-ММ-ДД", out)
        self.assertEqual(len(self.items), 12)

    def test_program_continues_after_error(self):  # TC-2.13
        out = run_app(self.items, add_answers(name="") + ["1", "0"])
        self.assertIn("Всего записей: 12", out)
        self.assertIn("До свидания", out)

    def test_bad_menu_input(self):  # TC-2.14
        out = run_app(self.items, ["abc", "", "99", "0"])
        self.assertEqual(out.count("Нет такого пункта"), 3)

    def test_future_items_show_message(self):
        out = run_app(self.items, ["3", "4", "5", "0"])
        self.assertEqual(out.count("будет реализован в спринте 3"), 3)

    def test_ctrl_d_in_menu_and_in_form(self):  # TC-2.15
        self.assertIn("Работа завершена", run_app(self.items, []))
        self.assertIn("Работа завершена", run_app(self.items, ["2", "INV-200", "ПК"]))
        self.assertEqual(len(self.items), 12)


if __name__ == "__main__":
    unittest.main()
