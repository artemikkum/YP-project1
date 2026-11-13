"""Хранение данных в JSON-файле (стандартный модуль json)."""
import json
import os
import time

DEFAULT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "inventory.json")


class StorageError(Exception):
    """Файл невозможно прочитать или записать."""


class CorruptedStorageError(StorageError):
    """Файл повреждён. Исходный файл не потерян: он переименован в backup_path."""

    def __init__(self, message, backup_path):
        super().__init__(message)
        self.backup_path = backup_path


def _backup_corrupted(path):
    backup = f"{path}.broken-{time.strftime('%Y%m%d-%H%M%S')}"
    n = 1
    while os.path.exists(backup):
        n += 1
        backup = f"{path}.broken-{time.strftime('%Y%m%d-%H%M%S')}-{n}"
    os.replace(path, backup)
    return backup


def load_items(path=DEFAULT_PATH):
    """Загружает записи. Нет файла или он пустой -> []. Повреждён -> CorruptedStorageError."""
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        raise StorageError(f"Не удалось прочитать файл {path}: {e}") from e
    if not text.strip():
        return []
    try:
        data = json.loads(text)
        if not isinstance(data, list) or not all(isinstance(x, dict) for x in data):
            raise ValueError("ожидался список записей")
    except ValueError as e:
        backup = _backup_corrupted(path)
        raise CorruptedStorageError(
            f"Файл данных повреждён ({e}). Копия сохранена: {backup}", backup
        ) from e
    return data


def save_items(items, path=DEFAULT_PATH):
    """Сохраняет записи атомарно: сначала во временный файл, затем замена."""
    folder = os.path.dirname(path)
    try:
        if folder:
            os.makedirs(folder, exist_ok=True)
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        os.replace(tmp, path)
    except OSError as e:
        raise StorageError(f"Не удалось сохранить файл {path}: {e}") from e
