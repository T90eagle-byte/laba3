# NEXT_PROMPT

Работаем в актуальной папке:

```text
C:\Users\User\DATA\Моя учеба\Web-razrab\pharmacy
```

Старый путь `C:\Users\User\Downloads\pharmacy` не использовать.

Перед началом:

1. Прочитать `WORK_CONTEXT.md`, `CHANGELOG.md`, `README_LR4.md`.
2. Проверить `git status --short`.
3. Не менять backend, web routes, SQLite-схему, Flask-WTF/CSRF и дизайн без необходимости.

Текущее состояние:

- Flask web-приложение из ЛР3 сохранено.
- SQLite база находится в `data/pharmacy.sqlite`.
- Импорт из ЛР1 через `data/catalog.pkl` сохранён.
- Пароли: Werkzeug hashes + legacy sha256 auto-upgrade.
- Session-cart сохранён.
- Owner-check заказов работает.
- Destructive web actions и logout защищены POST + CSRF.
- REST API ЛР4 добавлен в `app/api.py`.
- Console client ЛР4 добавлен в `console_client/` и работает через `requests.Session`.
- `requirements.txt` содержит `requests`.

REST API endpoints:

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

Следующий этап:

1. Финальная ручная проверка перед сдачей ЛР4.
2. При необходимости сделать commit/checkpoint.
3. Опционально расширить API админскими endpoints пользователей/товаров:
   - `GET/POST/PUT/DELETE /api/products`
   - `GET/POST/PUT/DELETE /api/users`

Правила:

- Консольный клиент не должен обращаться к SQLite или pickle напрямую.
- API не должен отдавать `password_hash`.
- SQL только через DB-API placeholders.
- Web CSRF не ломать.
- `PHARMACY_API_URL` должен оставаться способом настройки адреса API.
