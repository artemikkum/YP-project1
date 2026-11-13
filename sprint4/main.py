"""Консольное приложение «Система учёта инвентаря компьютерных классов».

Спринт 4: добавлено хранение данных в JSON (storage.py).
"""
import sys

import inventory as inv
import storage

MENU = """
===== Учёт инвентаря компьютерных классов =====
 1. Показать оборудование
 2. Добавить оборудование
 3. Найти оборудование
 4. Изменить запись
 5. Удалить запись
 0. Выход
"""


class UserQuit(Exception):
    """Ввод закончился (Ctrl+D / Ctrl+Z) - завершаем работу аккуратно."""


class App:
    def __init__(self, path=storage.DEFAULT_PATH, ask=input, say=print):
        self.path = path
        self._ask = ask
        self.say = say
        self.items = []

    # ---------- ввод/вывод ----------
    def ask(self, prompt):
        try:
            return self._ask(prompt).strip()
        except EOFError:
            raise UserQuit from None

    def confirm(self, prompt):
        return self.ask(prompt + " (да/нет): ").lower() in ("да", "д", "y", "yes")

    def load(self):
        try:
            self.items = storage.load_items(self.path)
        except storage.CorruptedStorageError as e:
            self.say(f"ВНИМАНИЕ: {e}\nПрограмма начнёт с пустого списка.")
            self.items = []
        except storage.StorageError as e:
            self.say(f"ОШИБКА: {e}")
            self.items = []

    def save(self):
        try:
            storage.save_items(self.items, self.path)
        except storage.StorageError as e:
            self.say(f"ОШИБКА: {e}")

    # ---------- пункты меню ----------
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
        self.save()
        self.say(f"Добавлено: {item['number']}")

    def find(self):
        self.say("Поиск: 1 - по номеру, 2 - по кабинету, 3 - по названию/типу")
        mode = self.ask("Выбор: ")
        if mode not in ("1", "2", "3"):
            self.say("Нужно ввести 1, 2 или 3.")
            return
        value = self.ask("Что искать: ")
        if not value:
            self.say("Пустой запрос. Введите значение для поиска.")
            return
        if mode == "1":
            found = inv.search(self.items, number=value)
        elif mode == "2":
            found = inv.search(self.items, room=value)
        else:
            found = inv.search(self.items, text=value)
        if not found:
            self.say("Не найдено")
        elif mode == "1":
            self.say(inv.format_item(found[0]))
        else:
            self.say(inv.format_table(found))

    def edit(self):
        number = self.ask("Номер изменяемой записи: ")
        item = inv.find_by_number(self.items, number)
        if item is None:
            self.say("Не найдено")
            return
        self.say(inv.format_item(item))
        self.say("Enter - оставить значение без изменений.")
        changes = {}
        for field in ("type", "name", "room", "state", "received", "responsible"):
            value = self.ask(f"{inv.FIELD_TITLES[field]} [{item[field] or '-'}]: ")
            if value:
                changes[field] = value
        if not changes:
            self.say("Изменений нет.")
            return
        try:
            inv.update_item(self.items, number, **changes)
        except inv.InventoryError as e:
            self.say(f"Ошибка: {e}")
            return
        self.save()
        self.say("Запись обновлена.")

    def delete(self):
        number = self.ask("Номер удаляемой записи: ")
        item = inv.find_by_number(self.items, number)
        if item is None:
            self.say("Не найдено")
            return
        self.say(inv.format_item(item))
        if not self.confirm("Удалить запись?"):
            self.say("Удаление отменено.")
            return
        inv.delete_item(self.items, number)
        self.save()
        self.say("Запись удалена.")

    # ---------- главный цикл ----------
    def run(self):
        self.load()
        actions = {
            "1": self.show, "2": self.add, "3": self.find,
            "4": self.edit, "5": self.delete,
        }
        try:
            while True:
                self.say(MENU)
                choice = self.ask("Пункт меню: ")
                if choice == "0":
                    self.say("До свидания!")
                    return
                action = actions.get(choice)
                if action is None:
                    self.say("Нет такого пункта. Введите число от 0 до 5.")
                    continue
                action()
        except (UserQuit, KeyboardInterrupt):
            self.say("\nРабота завершена.")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    path = argv[0] if argv else storage.DEFAULT_PATH
    App(path).run()


if __name__ == "__main__":
    main()
