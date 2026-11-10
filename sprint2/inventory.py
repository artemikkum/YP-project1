"""Логика учёта оборудования: проверка данных, добавление, номера (спринт 2).

Модуль не работает с вводом/выводом и сетью, поэтому все функции
тестируются напрямую (см. tests/test_inventory.py).
"""
import json
from datetime import date

STATES = ("исправно", "требует ремонта", "списано")
REQUIRED_FIELDS = ("number", "type", "name", "room", "state")
OPTIONAL_FIELDS = ("received", "responsible")
ALL_FIELDS = REQUIRED_FIELDS + OPTIONAL_FIELDS
FIELD_TITLES = {
    "number": "Инвентарный номер", "type": "Тип", "name": "Наименование",
    "room": "Кабинет", "state": "Состояние",
    "received": "Дата поступления", "responsible": "Ответственное лицо",
}


class InventoryError(ValueError):
    """Ошибка данных (пустое поле, неверное состояние или дата)."""


class DuplicateError(InventoryError):
    """Запись с таким номером уже существует."""


def load_demo(path):
    """Читает демонстрационные данные из JSON-файла."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_item(data):
    """Копия записи: только известные поля, строки без пробелов по краям."""
    item = {}
    for field in ALL_FIELDS:
        value = data.get(field, "")
        item[field] = "" if value is None else str(value).strip()
    item["state"] = item["state"].lower()
    return item


def validate_item(item):
    """Проверяет нормализованную запись. При ошибке бросает InventoryError."""
    for field in REQUIRED_FIELDS:
        if not item.get(field):
            raise InventoryError(f"Поле «{FIELD_TITLES[field]}» не должно быть пустым.")
    if item["state"] not in STATES:
        raise InventoryError("Недопустимое состояние. Допустимо: " + ", ".join(STATES) + ".")
    if item.get("received"):
        try:
            date.fromisoformat(item["received"])
        except ValueError:
            raise InventoryError(
                "Дата поступления должна быть в формате ГГГГ-ММ-ДД (например, 2024-09-01)."
            ) from None


def find_by_number(items, number):
    """Запись с указанным номером или None (регистр не важен)."""
    number = str(number).strip().lower()
    if not number:
        return None
    for item in items:
        if item["number"].lower() == number:
            return item
    return None


def add_item(items, data):
    """Проверяет и добавляет запись. Номер должен быть уникальным."""
    item = normalize_item(data)
    validate_item(item)
    if find_by_number(items, item["number"]) is not None:
        raise DuplicateError(f"Запись с номером {item['number']} уже существует.")
    items.append(item)
    return item


def next_number(items, prefix="INV-"):
    """Следующий свободный номер вида INV-013."""
    biggest = 0
    for item in items:
        number = item["number"]
        if number.upper().startswith(prefix) and number[len(prefix):].isdigit():
            biggest = max(biggest, int(number[len(prefix):]))
    return f"{prefix}{biggest + 1:03d}"


def format_table(items):
    """Текстовая таблица списка (используется в тестах и отладке)."""
    if not items:
        return "  (записей нет)"
    head = f"{'Номер':<9}{'Тип':<15}{'Наименование':<30}{'Каб.':<7}Состояние"
    rows = [head, "-" * len(head)]
    for i in items:
        rows.append(f"{i['number']:<9}{i['type']:<15}{i['name'][:28]:<30}{i['room']:<7}{i['state']}")
    return "\n".join(rows)
