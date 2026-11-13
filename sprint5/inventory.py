"""Логика учёта оборудования: проверка данных и операции над списком записей.

Модуль не работает с файлами и не обращается к вводу/выводу, поэтому
все функции легко тестируются (см. tests/test_inventory.py).
Запись об оборудовании - обычный словарь (dict), который хранится в JSON.
"""
from datetime import date

STATES = ("исправно", "требует ремонта", "списано")
REQUIRED_FIELDS = ("number", "type", "name", "room", "state")
OPTIONAL_FIELDS = ("received", "responsible")
ALL_FIELDS = REQUIRED_FIELDS + OPTIONAL_FIELDS
FIELD_TITLES = {
    "number": "Инвентарный номер",
    "type": "Тип",
    "name": "Наименование",
    "room": "Кабинет",
    "state": "Состояние",
    "received": "Дата поступления",
    "responsible": "Ответственное лицо",
}


class InventoryError(ValueError):
    """Ошибка бизнес-логики (неверные данные, дубликат, запись не найдена)."""


class NotFoundError(InventoryError):
    """Запись с таким номером не найдена."""


class DuplicateError(InventoryError):
    """Запись с таким номером уже существует."""


def normalize_item(data):
    """Возвращает копию записи: только известные поля, строки без пробелов по краям."""
    item = {}
    for field in ALL_FIELDS:
        value = data.get(field, "")
        if value is None:
            value = ""
        item[field] = str(value).strip()
    if item["state"]:
        item["state"] = item["state"].lower()
    return item


def validate_item(item):
    """Проверяет уже нормализованную запись. При ошибке бросает InventoryError."""
    for field in REQUIRED_FIELDS:
        if not item.get(field):
            raise InventoryError(f"Поле «{FIELD_TITLES[field]}» не должно быть пустым.")
    if item["state"] not in STATES:
        raise InventoryError(
            "Недопустимое состояние. Допустимо: " + ", ".join(STATES) + "."
        )
    if item.get("received"):
        try:
            date.fromisoformat(item["received"])
        except ValueError:
            raise InventoryError(
                "Дата поступления должна быть в формате ГГГГ-ММ-ДД (например, 2024-09-01)."
            ) from None


def find_by_number(items, number):
    """Возвращает запись с указанным номером или None (регистр не важен)."""
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
    """Предлагает следующий свободный номер вида INV-013."""
    biggest = 0
    for item in items:
        number = item["number"]
        if number.upper().startswith(prefix):
            tail = number[len(prefix):]
            if tail.isdigit():
                biggest = max(biggest, int(tail))
    return f"{prefix}{biggest + 1:03d}"


def search(items, number=None, room=None, text=None):
    """Поиск: по точному номеру, по кабинету или по части наименования/типа."""
    result = list(items)
    if number is not None and str(number).strip():
        found = find_by_number(items, number)
        result = [found] if found else []
    if room is not None and str(room).strip():
        wanted = str(room).strip().lower()
        result = [i for i in result if i["room"].lower() == wanted]
    if text is not None and str(text).strip():
        wanted = str(text).strip().lower()
        result = [
            i for i in result
            if wanted in i["name"].lower() or wanted in i["type"].lower()
        ]
    return result


def filter_items(items, room=None, state=None):
    """Фильтрация списка по кабинету и/или состоянию."""
    result = list(items)
    if room:
        result = [i for i in result if i["room"].lower() == room.strip().lower()]
    if state:
        result = [i for i in result if i["state"] == state.strip().lower()]
    return result


def update_item(items, number, /, **changes):
    """Изменяет поля записи. Менять инвентарный номер нельзя."""
    item = find_by_number(items, number)
    if item is None:
        raise NotFoundError(f"Запись с номером {number} не найдена.")
    if "number" in changes:
        raise InventoryError("Инвентарный номер изменять нельзя.")
    updated = dict(item)
    for field, value in changes.items():
        if field not in ALL_FIELDS:
            raise InventoryError(f"Неизвестное поле: {field}.")
        updated[field] = value
    updated = normalize_item(updated)
    validate_item(updated)
    item.update(updated)
    return item


def delete_item(items, number):
    """Удаляет запись и возвращает её. Если записи нет - InventoryError."""
    item = find_by_number(items, number)
    if item is None:
        raise NotFoundError(f"Запись с номером {number} не найдена.")
    items.remove(item)
    return item


def format_item(item):
    """Карточка оборудования в виде многострочного текста."""
    lines = []
    for field in ALL_FIELDS:
        value = item.get(field) or "-"
        lines.append(f"  {FIELD_TITLES[field]}: {value}")
    return "\n".join(lines)


def format_table(items):
    """Краткий табличный вывод списка."""
    if not items:
        return "  (записей нет)"
    head = f"{'Номер':<9}{'Тип':<15}{'Наименование':<30}{'Каб.':<7}Состояние"
    rows = [head, "-" * len(head)]
    for i in items:
        rows.append(
            f"{i['number']:<9}{i['type']:<15}{i['name'][:28]:<30}{i['room']:<7}{i['state']}"
        )
    return "\n".join(rows)
