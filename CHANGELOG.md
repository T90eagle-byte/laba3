# CHANGELOG

## 2026-06-04 — ЛР4 REST API и console client

- Добавлен REST API blueprint `api_bp` в `app/api.py` с prefix `/api`.
- `api_bp` зарегистрирован в `app/__init__.py`.
- Добавлены read-only API endpoints товаров:
  - `GET /api/products`
  - `GET /api/products/<id>`
- Добавлены auth API endpoints через Flask session cookies:
  - `POST /api/auth/login`
  - `POST /api/auth/logout`
  - `GET /api/auth/me`
- Login API переиспользует текущую Werkzeug/legacy-compatible password logic и не возвращает `password_hash`.
- Добавлены read/write API endpoints заказов с owner-check:
  - `GET /api/orders`
  - `GET /api/orders/<id>`
  - `POST /api/orders`
  - `PUT /api/orders/<id>`
  - `DELETE /api/orders/<id>`
- Обычный пользователь через API видит и меняет только свои заказы; админ может работать с любыми заказами.
- Добавлен `console_client/`:
  - `console_client/api_client.py`
  - `console_client/main.py`
  - `console_client/README.md`
- Консольный клиент использует `requests.Session`, REST endpoints `/api/...` и переменную `PHARMACY_API_URL` для настройки адреса.
- Консольный клиент больше не использует pickle или SQLite как источник данных.
- В `requirements.txt` добавлен `requests`.
- Добавлен `README_LR4.md` с описанием запуска, endpoints и примерами JSON.
- Пройдены проверки `py_compile`, Flask test client smoke и HTTP smoke console client.

## 2026-05-31 — финализация ЛР3

- D2C assets перенесены в `app/static`.
- Подключён общий стиль `app/static/css/app.css`.
- `base.tpl` обновлён под общий layout/header/nav.
- Дизайн перенесён на `login/register/products/cart/orders/profile`.
- Admin light styling выполнен.
- Добавлены категории, поиск и фильтр каталога.
- Централизован маппинг изображений товаров.
- Реализована session-корзина без новой Cart-модели.
- Старый flow `/orders/form/0` сохранён.
- Backend security стабилизирован: POST+CSRF, owner-check, POST logout.
- Пароли переведены на Werkzeug hashes с legacy sha256 auto-upgrade.
- Добавлен `data/catalog.pkl` для демонстрационного импорта из ЛР1.
