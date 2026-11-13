# Работа с Git в команде

Один репозиторий на команду, `main` всегда рабочая. Каждый участник делает **свои** коммиты.

## Начало (в первый день, делает QA)
```bash
git init
git add .
git commit -m "Каркас проекта: структура, меню, README"
git branch -M main
git remote add origin <ссылка на GitHub>     # если используете GitHub
git push -u origin main
```
Остальные: `git clone <ссылка>`.

## Ритм дня
```bash
git pull                                  # получить чужие изменения
git switch -c feature/add-item            # ветка под задачу
# ...работа...
git add <файлы>
git commit -m "Добавлена проверка уникального номера"
git push -u origin feature/add-item
# просмотр другим участником -> слияние
git switch main && git pull
git merge feature/add-item
git push
```

## Рекомендуемые ветки по спринтам
| Спринт | Ветки |
|---|---|
| 1 | `docs/user-stories`, `feature/menu`, `chore/setup-tests` |
| 2 | `feature/add-item`, `test/add-item`, `docs/data-rules` |
| 3 | `feature/search`, `feature/edit-delete`, `test/crud` |
| 4 | `feature/json-storage`, `test/storage`, `chore/dockerfile` |
| 5 | `fix/table-width`, `feature/filter`, `docs/user-guide` |
| 6 | `docs/final`, `chore/release` |

## Примеры хороших сообщений коммитов
- «Добавлен поиск по кабинету»
- «Исправлено: изменение номера давало TypeError»
- «Тесты: повреждённый JSON»

Плохо: «готово», «правки», «asdf».

## Конец спринта
```bash
git tag sprint-N
git log --oneline --graph --all    # показать историю
```
