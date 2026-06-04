# ЛР4: REST API и консольный клиент

## Цель

Лабораторная работа 4 добавляет к существующему WSGI-приложению аптеки REST API и отдельный консольный клиент. В результате одновременно работают:

- web-интерфейс Flask-приложения из ЛР3;
- REST API поверх того же Flask/SQLite backend;
- консольный клиент, который получает данные через REST API и не обращается напрямую к SQLite или pickle.

## Запуск Flask-сервера

Из корня проекта:

```powershell
python main.py
```

По умолчанию `main.py` использует порт `8000`, если переменная `PORT` не задана.

Для запуска на порту `5000`, который использует console client по умолчанию:

```powershell
$env:PORT=5000
python main.py
```

## Запуск консольного клиента

```powershell
python console_client/main.py
```

Клиент использует `requests.Session`, поэтому cookie-сессия Flask сохраняется после входа.

## Настройка адреса API

По умолчанию клиент обращается к:

```text
http://127.0.0.1:5000
```

Адрес можно изменить через переменную окружения:

```powershell
$env:PHARMACY_API_URL="http://127.0.0.1:8000"
python console_client/main.py
```

Это учитывает возможную смену адреса или идентификатора модуля: в клиенте не захардкожен полный путь к приложению, используются только относительные REST-маршруты `/api/...`.

## REST API endpoints

### Товары

```text
GET /api/products
GET /api/products/<id>
```

`GET /api/products` поддерживает query params:

```text
q=кур
category=Лекарства
```

### Авторизация

```text
POST /api/auth/login
POST /api/auth/logout
GET /api/auth/me
```

Авторизация работает через Flask session cookies. Пароли проверяются текущей Werkzeug/legacy-compatible логикой. `password_hash` в JSON не возвращается.

### Заказы

```text
GET    /api/orders
GET    /api/orders/<id>
POST   /api/orders
PUT    /api/orders/<id>
DELETE /api/orders/<id>
```

Обычный пользователь видит и изменяет только свои заказы. Администратор может работать с любыми заказами.

## Формат JSON

Успех:

```json
{
  "ok": true,
  "data": {}
}
```

Ошибка:

```json
{
  "ok": false,
  "error": "Описание ошибки"
}
```

## Примеры запросов

### Вход

```json
POST /api/auth/login
{
  "login": "admin",
  "password": "admin"
}
```

Ответ:

```json
{
  "ok": true,
  "data": {
    "user": {
      "id": 2,
      "login": "admin",
      "name": "Admin",
      "surname": "",
      "patronymic": "",
      "address": "",
      "is_admin": true
    }
  }
}
```

### Создание заказа

```json
POST /api/orders
{
  "product_ids": [10, 12],
  "payment": "наличные"
}
```

Ответ:

```json
{
  "ok": true,
  "data": {
    "id": 23,
    "user_id": 2,
    "payment": "наличные",
    "items": [
      {
        "id": 10,
        "name": "Рисостанон",
        "dosage": "250, мг",
        "category": "Лекарства",
        "price": 1250.0,
        "in_stock": true,
        "image": "8af2af4ea1fe6457c7dfbeb1d53e527d1ce6b985.png"
      }
    ],
    "total": 3250.0
  }
}
```

## Проверка общей базы web и console

1. Запустить Flask-сервер.
2. Запустить `python console_client/main.py`.
3. Войти через консоль.
4. Создать заказ в консольном клиенте.
5. Открыть web-страницу `/orders` под тем же пользователем.
6. Новый заказ должен быть виден в web-интерфейсе, потому что web и console работают с одной SQLite-базой через один Flask backend.

## Важное отличие от ЛР2

Консольный клиент больше не использует `catalog.pkl` как источник данных и не обращается к SQLite напрямую. Все операции выполняются через HTTP REST API Flask-приложения.

## Проверка

```powershell
python -m py_compile main.py app/__init__.py app/pharmacy.py app/forms.py app/api.py console_client/api_client.py console_client/main.py
```

Также проверены:

- все API endpoints товаров, авторизации и заказов;
- web routes `/products`, `/login`, `/orders`, `/cart`, `/profile`, `/admin`;
- owner-check заказов в API;
- отсутствие `password_hash` в JSON-ответах;
- работа консольного клиента через HTTP REST API.
