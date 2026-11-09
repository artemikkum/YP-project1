"""Модель записи об оборудовании и вывод списка (спринт 1)."""
import json

STATES = ("исправно", "требует ремонта", "списано")
REQUIRED_FIELDS = ("number", "type", "name", "room", "state")


def load_demo(path):
    """Читает демонстрационные данные из JSON-файла."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def format_table(items):
    """Краткий табличный вывод списка оборудования."""
    if not items:
        return "  (записей нет)"
    head = f"{'Номер':<9}{'Тип':<15}{'Наименование':<30}{'Каб.':<7}Состояние"
    rows = [head, "-" * len(head)]
    for i in items:
        rows.append(
            f"{i['number']:<9}{i['type']:<15}{i['name'][:28]:<30}{i['room']:<7}{i['state']}"
        )
    return "\n".join(rows)
