import os
from urllib.parse import urljoin

import requests


DEFAULT_BASE_URL = "http://127.0.0.1:5000"
ENV_BASE_URL = "PHARMACY_API_URL"


class ApiError(Exception):
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class PharmacyApiClient:
    def __init__(self, base_url=None, session=None, timeout=10):
        self.base_url = (base_url or os.environ.get(ENV_BASE_URL) or DEFAULT_BASE_URL).strip().rstrip("/")
        self.session = session or requests.Session()
        self.timeout = timeout

    def _url(self, path):
        if not path.startswith("/"):
            path = "/" + path
        if self.base_url.endswith("/api") and path.startswith("/api/"):
            path = path[4:]
        return urljoin(self.base_url + "/", path.lstrip("/"))

    def _request(self, method, path, **kwargs):
        try:
            response = self.session.request(
                method,
                self._url(path),
                timeout=self.timeout,
                **kwargs,
            )
        except requests.RequestException as exc:
            raise ApiError(f"Сервер недоступен: {exc}") from exc

        try:
            payload = response.json()
        except ValueError as exc:
            raise ApiError(f"Сервер вернул не JSON ответ, HTTP {response.status_code}", response.status_code) from exc

        if not isinstance(payload, dict):
            raise ApiError("Некорректный JSON-ответ API", response.status_code)

        if not payload.get("ok"):
            message = payload.get("error") or f"Ошибка API, HTTP {response.status_code}"
            raise ApiError(message, response.status_code)

        return payload.get("data")

    def login(self, login, password):
        return self._request("POST", "/api/auth/login", json={"login": login, "password": password})

    def logout(self):
        return self._request("POST", "/api/auth/logout")

    def me(self):
        return self._request("GET", "/api/auth/me")

    def products(self, q=None, category=None):
        params = {}
        if q:
            params["q"] = q
        if category and category != "Все":
            params["category"] = category
        return self._request("GET", "/api/products", params=params)

    def product(self, product_id):
        return self._request("GET", f"/api/products/{product_id}")

    def orders(self):
        return self._request("GET", "/api/orders")

    def order(self, order_id):
        return self._request("GET", f"/api/orders/{order_id}")

    def create_order(self, product_ids, payment):
        return self._request(
            "POST",
            "/api/orders",
            json={"product_ids": product_ids, "payment": payment},
        )

    def update_order(self, order_id, product_ids, payment):
        return self._request(
            "PUT",
            f"/api/orders/{order_id}",
            json={"product_ids": product_ids, "payment": payment},
        )

    def delete_order(self, order_id):
        return self._request("DELETE", f"/api/orders/{order_id}")
