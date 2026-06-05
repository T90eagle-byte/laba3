# WORK_CONTEXT

## Актуальное состояние

Проект находится в:

```text
C:\Users\User\DATA\Моя учеба\Web-razrab\pharmacy
```

Это учебное WSGI-приложение аптеки/картотеки на Flask. Проект развивает консольную картотеку из ЛР2, web-интерфейс из ЛР3 и теперь содержит REST API + консольный REST-клиент для ЛР4.

## Стек и структура

- Flask-приложение создаётся в `app/__init__.py`.
- WSGI entrypoint доступен через `from app import app` и `main.py`.
- SQLite база: `data/pharmacy.sqlite`.
- Импортный демонстрационный файл ЛР1: `data/catalog.pkl`.
- Шаблоны: `app/templates`.
- Static: `app/static`.
- Основная web/backend-логика: `app/pharmacy.py`.
- Flask-WTF формы: `app/forms.py`.
- REST API ЛР4: `app/api.py`.
- Консольный REST-клиент: `console_client/`.

## Состояние ЛР3

- Flask, Flask-Login, Flask-WTF используются и сохранены.
- Админка сохранена.
- Импорт из ЛР1 сохранён.
- Дизайн из Pixso D2C перенесён на `login/register/products/cart/orders/profile`.
- Admin light styling выполнен.
- Каталог поддерживает поиск `q` и фильтр `category`.
- Session-корзина реализована без Cart-модели и без миграций.
- Старый flow `/orders/form/0` сохранён.

## Безопасность

- Пароли сохраняются через Werkzeug `generate_password_hash` / `check_password_hash`.
- Legacy `sha256` поддерживается и автоапгрейдится при успешном входе.
- SQL использует DB-API placeholders `?`.
- Destructive web actions выполняются через POST + CSRF.
- Logout web работает через POST + CSRF.
- Owner-check заказов закрыт: обычный пользователь не может открыть, изменить или удалить чужой заказ.
- `password_hash` не возвращается в REST JSON.

## REST API ЛР4

Добавлен `app/api.py` с blueprint `api_bp` и prefix `/api`.

Endpoints:

```text
GET    /api/products
GET    /api/products/<id>
POST   /api/auth/login
POST   /api/auth/logout
GET    /api/auth/me
GET    /api/orders
GET    /api/orders/<id>
POST   /api/orders
PUT    /api/orders/<id>
DELETE /api/orders/<id>
```

Формат ответов:

```json
{"ok": true, "data": {}}
{"ok": false, "error": "..."}
```

API использует Flask session cookies, поэтому консольный клиент работает через `requests.Session`.

## Console client ЛР4

Добавлена папка `console_client/`:

- `console_client/api_client.py` — HTTP-клиент для REST API;
- `console_client/main.py` — интерактивное меню;
- `console_client/README.md` — краткая инструкция.

Клиент:

- не обращается к SQLite напрямую;
- не использует pickle как источник данных;
- использует только `/api/...`;
- берёт адрес из `PHARMACY_API_URL` или использует `http://127.0.0.1:5000`;
- поддерживает login, каталог, поиск, фильтр категории, просмотр/создание/изменение/удаление заказов, logout.

## Зависимости

`requirements.txt` содержит:

```text
Flask
Flask-Login
Flask-WTF
requests
```

## Последние проверки

- `py_compile` прошёл для Flask и console client файлов.
- API endpoints товаров, auth и orders проверены через Flask test client.
- Web routes `/products`, `/login`, `/orders`, `/cart`, `/profile`, `/admin` отвечают.
- Owner-check API заказов проверен: чужой PUT/DELETE для обычного пользователя возвращает 403.
- Консольный клиент проверен через реальный HTTP REST API на временно запущенном Flask-сервере.

## Дальше

Основной следующий этап: финальная сдача ЛР4. Опционально можно расширить API админскими CRUD endpoints для пользователей и товаров, но это не требуется для основного пользовательского сценария консольного клиента.

## Важные запреты

- Не ломать Flask / Flask-Login / Flask-WTF.
- Не ломать web routes, Jinja, WTForms, CSRF, `module_url` / `url_for`.
- Не менять SQLite-схему без необходимости.
- Не возвращать `password_hash` наружу.
- Не возвращать консоль к прямой работе с SQLite или pickle.
