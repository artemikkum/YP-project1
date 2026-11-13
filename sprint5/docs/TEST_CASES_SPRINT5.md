# Тест-кейсы спринта 5

| ID | Функция | Шаги | Ожидаемый результат | Автотест |
|---|---|---|---|---|
| TC-5.1 | Изменение | `update_item(..., responsible="", received="")` | Необязательные поля очищены | `test_clear_optional_field_with_empty_string` |
| TC-5.2 | Изменение | `update_item(..., room="")` | Ошибка, кабинет не изменился | `test_cannot_clear_required_field` |
| TC-5.3 | Изменение | Пункт 4: дата и ответственный → `-` | Поля очищены и сохранены в файл | `test_edit_dash_clears_optional_fields` |
| TC-5.4 | Изменение | Пункт 4: кабинет → `-` | Ошибка «обязательное», данные целы | `test_edit_dash_on_required_field_is_error` |
| TC-5.5 | Фильтр | Пункт 6: кабинет `101` | Найдено: 5 | `test_filter_by_room` |
| TC-5.6 | Фильтр | Пункт 6: «требует ремонта» | Найдено: 2 (INV-004, INV-007) | `test_filter_by_state` |
| TC-5.7 | Фильтр | Пункт 6: кабинет `102` + «исправно» | Найдено: 3 | `test_filter_by_room_and_state` |
| TC-5.8 | Фильтр | Пункт 6: состояние «сломано» | Сообщение со списком допустимых | `test_filter_unknown_state` |
| TC-5.9 | Фильтр | Без условий; ничего не найдено | 12 записей; «Найдено: 0» | `test_filter_without_conditions_shows_all`, `test_filter_nothing_found` |
| TC-5.10 | Логика | `filter_items`, нормализация состояния при изменении | Исходный список не меняется | `test_filter_by_room_and_state` (логика), `test_filter_does_not_change_source_list`, `test_update_normalizes_state` |
| TC-5.11 | Ограничение | Удалить последнюю запись и запросить следующий номер | Номер выдаётся повторно (известное ограничение N-5.1) | `test_number_can_be_reused_after_delete_known_limitation` |
| TC-5.12 | Регресс | Все тесты спринтов 1-4 | Проходят | все остальные тесты |
