"""Консольное приложение «Система учёта инвентаря компьютерных классов».

Спринт 2: просмотр оборудования и добавление с проверкой данных.
Данные пока хранятся только в памяти: после выхода добавленные записи
пропадут (сохранение в JSON появится в спринте 4).
"""
import os

import inventory as inv

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "inventory.json")

MENU = """
===== Учёт инвентаря компьютерных классов =====
 1. Показать оборудование
 2. Добавить оборудование
 3. Найти оборудование      (спринт 3)
 4. Изменить запись         (спринт 3)
 5. Удалить запись          (спринт 3)
 0. Выход
"""

PLANNED = {"3": "спринте 3", "4": "спринте 3", "5": "спринте 3"}


class UserQuit(Exception):
    """Ввод закончился (Ctrl+D / Ctrl+Z) - завершаем работу аккуратно."""


class App:
    def __init__(self, items, ask=input, say=print):
        self.items = items
        self._ask = ask
        self.say = say

    def ask(self, prompt):
        try:
            return self._ask(prompt).strip()
        except EOFError:
            raise UserQuit from None

    def show(self):
        self.say(inv.format_table(self.items))
        self.say(f"Всего записей: {len(self.items)}")

    def add(self):
        self.say("Добавление оборудования (* - обязательное поле).")
        number = self.ask("Инвентарный номер (Enter - присвоить автоматически): ")
        if not number:
            number = inv.next_number(self.items)
            self.say(f"Присвоен номер: {number}")
        data = {
            "number": number,
            "type": self.ask("Тип * (ПК/монитор/принтер...): "),
            "name": self.ask("Наименование *: "),
            "room": self.ask("Кабинет *: "),
            "state": self.ask("Состояние * (" + "/".join(inv.STATES) + "): "),
            "received": self.ask("Дата поступления ГГГГ-ММ-ДД (Enter - пропустить): "),
            "responsible": self.ask("Ответственное лицо (Enter - пропустить): "),
        }
        try:
            item = inv.add_item(self.items, data)
        except inv.InventoryError as e:
            self.say(f"Ошибка: {e} Запись не добавлена.")
            return
        self.say(f"Добавлено: {item['number']}")

    def run(self):
        try:
            while True:
                self.say(MENU)
                choice = self.ask("Пункт меню: ")
                if choice == "0":
                    self.say("До свидания!")
                    return
                if choice == "1":
                    self.show()
                elif choice == "2":
                    self.add()
                elif choice in PLANNED:
                    self.say(f"Этот пункт будет реализован в {PLANNED[choice]}.")
                else:
                    self.say("Нет такого пункта. Введите число от 0 до 5.")
        except (UserQuit, KeyboardInterrupt):
            self.say("\nРабота завершена.")


def main():
    try:
        items = inv.load_demo(DATA_FILE)
    except (OSError, ValueError) as e:
        print(f"Не удалось загрузить демонстрационные данные: {e}")
        items = []
    App(items).run()


if __name__ == "__main__":
    main()
