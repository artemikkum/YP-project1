# Тест-кейсы спринта 3

| ID | Функция | Шаги | Ожидаемый результат | Автотест |
|---|---|---|---|---|
| TC-3.1 | Поиск | Пункт 3 → 1 → `INV-004` | Карточка: кабинет 101, «требует ремонта» | `test_find_by_number_shows_card` |
| TC-3.2 | Поиск | Пункт 3 → 1 → `INV-999` | «Не найдено» | `test_find_by_number_not_found` |
| TC-3.3 | Поиск | Пункт 3 → 1 → пустой ввод | «Пустой запрос», программа продолжает работу | `test_find_empty_query_does_not_crash` |
| TC-3.4 | Поиск | Пункт 3 → 2 → `102` | Таблица из 4 устройств кабинета | `test_find_by_room_lists_all_devices` |
| TC-3.5 | Поиск | Повторить один и тот же поиск | Результат тот же | `test_repeated_search_same_result` |
| TC-3.6 | Изменение | Пункт 4: кабинет `205`, состояние «требует ремонта», остальное Enter | Поля обновлены, остальные без изменений | `test_edit_room_and_state` |
| TC-3.7 | Изменение | Пункт 4: состояние «сломано» | Ошибка, старые данные сохранены | `test_edit_invalid_state_keeps_old_data` |
| TC-3.8 | Удаление | Пункт 5 → `INV-012` → «да» | Запись удалена, остаётся 11 | `test_delete_confirmed` |
| TC-3.9 | Удаление | Пункт 5 → `INV-012` → «нет» (и мусорный ответ) | Запись остаётся | `test_delete_cancelled`, `test_delete_garbage_answer_cancels` |
| TC-3.10 | Устойчивость | Неверный номер в поиске, изменении, удалении | 3 × «Не найдено» | `test_delete_not_found`, `test_edit_not_found`, `test_not_found_everywhere` |
| TC-3.11 | Сценарий | добавить → найти → изменить → удалить | Все шаги проходят, записей снова 12 | `test_full_user_scenario` |
| TC-3.12 | Логика | `search`, `update_item`, `delete_item` на граничных значениях (пустой номер, неизвестное поле, смена номера) | Ошибки `InventoryError`, данные не портятся | `SearchTests`, `UpdateDeleteTests` в `test_inventory.py` |
