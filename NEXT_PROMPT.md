# NEXT_PROMPT

Ты работаешь с существующим Flask-проектом аптеки.

Перед началом:
1. Прочитай `WORK_CONTEXT.md` и `CHANGELOG.md`.
2. Проверь `git status`.

Ключевые ограничения:
- Не менять backend без необходимости.
- Не переписывать проект с нуля.
- Не ломать Flask / Flask-Login / Flask-WTF.
- Не ломать Jinja, WTForms, `module_url` / `url_for`.
- Не вводить миграции и не создавать Cart-модель в БД без отдельного согласования.

Главная цель сессии:
Перейти к pixel-perfect переносу дизайна из `design_export` (и PDF, если будет приложен) в существующие шаблоны Flask.

Работать по этапам:
1. `login` / `register`
2. `catalog`
3. `cart`
4. `orders`
5. `profile`
6. `admin` (только light styling, без ломки CRUD)

Правила переноса:
- Не копировать D2C HTML целиком.
- Адаптировать дизайн в существующие Jinja-шаблоны.
- Сохранять текущую backend-логику, form actions и имена полей.

После каждого этапа:
- Кратко перечислять измененные файлы.
- Проверять, что сценарии страниц не сломаны.
- Прогонять минимум:
  - `python -m py_compile main.py`
  - `python -m py_compile app/pharmacy.py`
  - `python -m py_compile app/forms.py`
