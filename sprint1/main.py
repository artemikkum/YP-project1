"""Консольное приложение «Система учёта инвентаря компьютерных классов».

Спринт 1: меню и пункт «Показать оборудование» на демонстрационных данных.
Остальные пункты появятся в следующих спринтах.
"""
import os

import inventory as inv

DATA_FILE = os.path.join("data", "inventory.json")

MENU = """
===== Учёт инвентаря компьютерных классов =====
 1. Показать оборудование
 2. Добавить оборудование   (спринт 2)
 3. Найти оборудование      (спринт 3)
 4. Изменить запись         (спринт 3)
 5. Удалить запись          (спринт 3)
 0. Выход
"""

PLANNED = {"2": "спринте 2", "3": "спринте 3", "4": "спринте 3", "5": "спринте 3"}


def show(items):
    print(inv.format_table(items))
    print(f"Всего записей: {len(items)}")


def main():
    try:
        items = inv.load_demo(DATA_FILE)
    except (OSError, ValueError) as e:
        print(f"Не удалось загрузить демонстрационные данные: {e}")
        items = []
    while True:
        print(MENU)
        try:
            choice = input("Пункт меню: ").strip()
        except EOFError:
            print("\nРабота завершена.")
            return
        if choice == "0":
            print("До свидания!")
            return
        if choice == "1":
            show(items)
        elif choice in PLANNED:
            print(f"Этот пункт будет реализован в {PLANNED[choice]}.")
        else:
            print("Нет такого пункта. Введите число от 0 до 5.")


if __name__ == "__main__":
    main()
