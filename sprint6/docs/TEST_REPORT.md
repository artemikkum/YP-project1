# Отчёт о тестировании

**Версия:** финальная (спринт 6) • **Python:** 3.12.3 • **ОС:** Linux

## Результат прогона
Проект скопирован в чистую папку и запущен без подготовки:

```
python -m unittest discover -s tests -t . -v
test_bad_menu_input ... ok
test_bad_search_mode ... ok
test_ctrl_d_exits_cleanly ... ok
test_delete_cancelled ... ok
test_delete_confirmed ... ok
test_delete_garbage_answer_cancels ... ok
test_delete_not_found ... ok
test_duplicate_rejected ... ok
test_edit_invalid_state_keeps_old_data ... ok
test_edit_not_found ... ok
test_edit_room_and_state ... ok
test_edit_without_changes ... ok
test_find_by_number_not_found ... ok
test_find_by_number_shows_card ... ok
test_find_by_room_lists_all_devices ... ok
test_find_by_room_not_found ... ok
test_find_by_text_case_insensitive ... ok
test_find_empty_query_does_not_crash ... ok
test_full_user_scenario ... ok
test_not_found_everywhere ... ok
test_repeated_search_same_result ... ok
test_show_and_add ... ok
test_edit_dash_clears_optional_fields ... ok
test_edit_dash_on_required_field_is_error ... ok
test_filter_by_room ... ok
test_filter_by_room_and_state ... ok
test_filter_by_state ... ok
test_filter_nothing_found ... ok
test_filter_unknown_state ... ok
test_filter_without_conditions_shows_all ... ok
test_changes_survive_restart ... ok
test_corrupted_file_on_start ... ok
test_data_survives_restart ... ok
test_demo_data_file_is_valid ... ok
test_failed_add_is_not_saved ... ok
test_missing_file_starts_empty_and_is_created ... ok
test_add_bad_and_good_date ... ok
test_add_bad_state ... ok
test_add_duplicate_number ... ok
test_add_empty_required_field ... ok
test_add_ok ... ok
test_add_strips_spaces_and_lowers_state ... ok
test_optional_fields_may_be_empty ... ok
test_unknown_fields_are_dropped ... ok
test_long_type_does_not_stick_to_next_column ... ok
test_find_by_number ... ok
test_next_number_after_existing ... ok
test_next_number_empty ... ok
test_filter_by_room_and_state ... ok
test_find_existing ... ok
test_find_missing_and_empty ... ok
test_search_by_room ... ok
test_search_by_text ... ok
test_search_repeated ... ok
test_cannot_clear_required_field ... ok
test_clear_optional_field_with_empty_string ... ok
test_filter_does_not_change_source_list ... ok
test_number_can_be_reused_after_delete_known_limitation ... ok
test_update_normalizes_state ... ok
test_delete_missing ... ok
test_delete_ok ... ok
test_update_invalid_keeps_old_data ... ok
test_update_missing ... ok
test_update_number_forbidden ... ok
test_update_state_and_room ... ok
test_demo_data_has_at_least_5_records ... ok
test_every_record_has_required_fields ... ok
test_table_shows_all_numbers_and_empty_list ... ok
test_corrupted_json_is_backed_up ... ok
test_empty_file ... ok
test_missing_file_gives_empty_list ... ok
test_save_and_load_roundtrip ... ok
test_save_leaves_no_tmp_file ... ok
test_unicode_is_readable_in_file ... ok
test_wrong_structure_is_corrupted ... ok

Ran 75 tests ... OK
```

**Итого: 75 тестов, 75 пройдено, 0 упавших.** Требование «минимум 10 тестов» выполнено.

> Тесты написаны на `unittest.TestCase`, поэтому так же выполняются командой `python -m pytest`. Прогон выше сделан через `unittest`; на учебном компьютере выполните `python -m pytest -v` и приложите свой вывод.

## Покрытие по областям
| Область | Тестов | Файл |
|---|---|---|
| Сценарии меню, перезапуски, фильтр | 36 | `tests/test_cli.py` |
| Логика (проверка, поиск, изменение, удаление, фильтр) | 29 | `tests/test_inventory.py` |
| Демо-данные | 3 | `tests/test_sprint1.py` |
| JSON-хранение | 7 | `tests/test_storage.py` |

Описание тест-кейсов - `docs/TEST_CASES*.md`, дефекты - `docs/DEFECTS.md`.

## Регрессия
Финальный прогон всего набора в чистой копии проекта: все тесты спринтов 1-5 проходят.

## Ручные проверки
- Запуск `python main.py` на копии данных: просмотр, поиск по номеру и кабинету, изменение, удаление с подтверждением, фильтр, неверный пункт меню, выход через `0` и Ctrl+D.
- Перезапуск программы: добавленные, изменённые и удалённые записи сохраняются.
- Повреждённый файл: предупреждение и копия `*.broken-<дата>`.

## Не проверено
- **Docker:** на машине подготовки Docker не установлен, `Dockerfile` не собирался. Проверьте: `docker build -t inventory .` (необязательная часть).
- Работа на Windows/macOS: код использует только стандартные кроссплатформенные модули, но запуск там не выполнялся.
- Установка pytest через `pip`: без доступа к сети не проверялась.

## Известные ограничения
См. README.md → «Ограничения».
