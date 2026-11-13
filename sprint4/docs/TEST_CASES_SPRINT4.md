# Тест-кейсы спринта 4

| ID | Функция | Шаги | Ожидаемый результат | Автотест |
|---|---|---|---|---|
| TC-4.1 | Хранение | Добавить запись, выйти, запустить снова, найти | Запись на месте | `test_data_survives_restart` |
| TC-4.2 | Хранение | Изменить и удалить запись, перезапуск | Изменения сохранены | `test_changes_survive_restart` |
| TC-4.3 | Хранение | Файла нет → пункт 1; затем добавить запись | Пустой список без сбоя; файл создаётся | `test_missing_file_starts_empty_and_is_created` |
| TC-4.4 | Хранение | Испорченный JSON при старте | Предупреждение, копия `*.broken-*`, пустой список | `test_corrupted_file_on_start` |
| TC-4.5 | Данные | Проверить файл примеров | ≥ 10 корректных записей, уникальные номера | `test_demo_data_file_is_valid` |
| TC-4.6 | storage | `load_items`, файла нет | Пустой список | `test_missing_file_gives_empty_list` |
| TC-4.7 | storage | Сохранить и загрузить; кириллица | Данные совпадают, текст читаем в файле | `test_save_and_load_roundtrip`, `test_unicode_is_readable_in_file` |
| TC-4.8 | storage | Пустой файл | Пустой список | `test_empty_file` |
| TC-4.9 | storage | Битый JSON и неверная структура | `CorruptedStorageError`, копия файла сохранена | `test_corrupted_json_is_backed_up`, `test_wrong_structure_is_corrupted` |
| TC-4.10 | storage | Сохранение | Временный `.tmp` не остаётся | `test_save_leaves_no_tmp_file` |
| TC-4.11 | Хранение | Неудачное добавление (пустой кабинет) | Файл не изменяется | `test_failed_add_is_not_saved` |
| TC-4.12 | Регресс | Все тесты меню спринта 3 через временный файл | Результаты прежние | `CliTests` в `test_cli.py` |
