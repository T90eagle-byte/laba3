<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Invalidhelp</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: Arial, sans-serif; background: #e0f7f4; min-height: 100vh; }

nav {
  background: #e0f7f4; padding: 12px 28px;
  display: flex; align-items: center; gap: 16px;
  border-bottom: 1px solid #b2dfdb;
}
.nav-logo {
  background: #00BFA5; color: #fff; font-weight: bold;
  font-size: 1.05rem; padding: 8px 20px; border-radius: 24px;
  text-decoration: none;
}
.nav-catalog {
  background: #7B1FA2; color: #fff; font-weight: bold;
  padding: 8px 18px; border-radius: 24px; text-decoration: none; font-size: .92rem;
}
.nav-link { color: #37474F; text-decoration: none; font-size: .9rem;
            padding: 6px 12px; border-radius: 16px; }
.nav-link:hover { background: #b2dfdb; }
.nav-spacer { flex: 1; }
.nav-avatar {
  width: 38px; height: 38px; border-radius: 50%;
  background: #90A4AE; color: #fff; font-weight: bold;
  display: flex; align-items: center; justify-content: center;
  font-size: .88rem; text-decoration: none;
}

.container { max-width: 980px; margin: 32px auto; padding: 0 24px; }
h1 { font-size: 1.55rem; color: #37474F; margin-bottom: 20px; }
h2 { font-size: 1.15rem; color: #37474F; margin-bottom: 14px; }

.btn {
  display: inline-block; padding: 9px 22px; border-radius: 24px;
  font-size: .9rem; font-weight: bold; text-decoration: none;
  border: none; cursor: pointer; transition: opacity .2s;
}
.btn:hover { opacity: .85; }
.btn-primary { background: #00BFA5; color: #fff; }
.btn-purple  { background: #7B1FA2; color: #fff; }
.btn-danger  { background: #e53935; color: #fff; }
.btn-gray    { background: #90A4AE; color: #fff; }
.btn-sm { padding: 5px 14px; font-size: .82rem; }

table { width: 100%; border-collapse: collapse; background: #fff;
        border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px #0001; }
th { background: #7B1FA2; color: #fff; padding: 11px 14px;
     text-align: left; font-size: .88rem; }
td { padding: 10px 14px; border-bottom: 1px solid #f0f0f0;
     font-size: .9rem; color: #37474F; vertical-align: middle; }
tr:last-child td { border-bottom: none; }
tr:hover td { background: #fafafa; }

.badge-green { background:#E8F5E9; color:#2E7D32; padding:3px 10px; border-radius:12px; font-size:.78rem; }
.badge-red   { background:#FFEBEE; color:#C62828; padding:3px 10px; border-radius:12px; font-size:.78rem; }

.form-card { background:#fff; border-radius:14px; padding:28px;
             max-width:500px; box-shadow:0 2px 8px #0001; }
.form-group { margin-bottom:16px; }
label { display:block; font-size:.85rem; color:#546E7A; margin-bottom:5px; }
input[type=text], input[type=number], input[type=password], select {
  width:100%; padding:9px 16px; border:1.5px solid #b2dfdb;
  border-radius:24px; font-size:.95rem; outline:none; transition:border .2s;
}
input:focus, select:focus { border-color: #7B1FA2; }
.form-actions { display:flex; gap:12px; margin-top:20px; }

.info-box { background:#E8F5E9; border-left:4px solid #00BFA5;
            padding:14px 18px; border-radius:8px; margin-bottom:20px;
            color:#2E7D32; font-size:.93rem; }
.error-box { background:#FFEBEE; border-left:4px solid #e53935;
             padding:12px 18px; border-radius:8px; margin-bottom:18px;
             color:#C62828; font-size:.9rem; }
.empty { color:#90A4AE; font-style:italic; margin-top:16px; }
</style>
</head>
<body>
<nav>
  <a class="nav-logo" href="{{ module_url('products') }}">Invalidhelp</a>
  <a class="nav-catalog" href="{{ module_url('products') }}">≡ Каталог</a>
  {% if current_user.is_authenticated %}
    <a class="nav-link" href="{{ module_url('my_orders') }}">Мои заказы</a>
    {% if current_user.is_admin %}
      <a class="nav-link" href="{{ module_url('admin') }}">Админка</a>
    {% endif %}
  {% endif %}
  <div class="nav-spacer"></div>
  {% if current_user.is_authenticated %}
    <a class="nav-link" href="{{ module_url('my_orders') }}">Мои заказы</a>
    <a class="nav-avatar" href="{{ module_url('profile') }}"
       title="Настройки профиля">{{ current_user.initials() }}</a>
  {% else %}
    <a class="nav-link" href="{{ module_url('login') }}">Войти</a>
    <a class="btn btn-primary btn-sm" href="{{ module_url('register') }}">Регистрация</a>
  {% endif %}
</nav>
<div class="container">
  {% block content %}{% endblock %}
</div>
</body>
</html>
