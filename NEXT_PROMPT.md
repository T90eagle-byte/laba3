# NEXT_PROMPT

## Final Continuation Prompt (2026-05-31)

Ты работаешь с существующим Flask-проектом по пути:
`C:\Users\User\DATA\Моя учеба\Web-razrab\pharmacy`

Перед началом:
1. Прочитай `WORK_CONTEXT.md` и `CHANGELOG.md`.
2. Выполни `git status --short`.
3. Убедись, что backend не меняется без отдельной необходимости.

Текущее состояние:
- Backend стабилизирован.
- Используются Flask / Flask-Login / Flask-WTF / SQLite.
- Пароли: Werkzeug hash + legacy sha256 auto-upgrade.
- Корзина: session-based (`/cart`, `/cart/add`, `/cart/remove`, `/cart/checkout`).
- Owner-check заказов и POST+CSRF для destructive actions уже закрыты.
- Logout работает через POST + CSRF.
- Дизайн уже перенесён на `login/register/products/cart/orders/profile`.
- Для админки выполнен light styling.
- Для демонстрационного импорта ЛР1 доступен `data/catalog.pkl`.

Ограничения:
- Не ломать Flask/Jinja/WTForms/module_url/url_for.
- Не ломать routes, CSRF, session-cart, owner-check, admin CRUD, import.
- Не менять SQLite-схему и не делать миграции без отдельного запроса.

Следующий этап (если продолжаем):
1. Финальная ручная визуальная сверка pixel-perfect против D2C/PDF.
2. Точечная доводка spacing/typography/mobile без изменения backend.
3. Финальный checkpoint и подготовка к сдаче (документация + чистый git status tracked-файлов).

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
