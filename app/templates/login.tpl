<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Вход — Invalidhelp</title>
<style>
* { box-sizing:border-box; margin:0; padding:0; }
body { font-family:Arial,sans-serif; background:#e0f7f4;
       display:flex; align-items:center; justify-content:center; min-height:100vh; }
.card { background:#fff; border-radius:20px; padding:44px 48px;
        width:100%; max-width:400px; box-shadow:0 4px 20px #0001; text-align:center; }
h2 { color:#37474F; margin-bottom:28px; font-size:1.25rem; }
.form-group { margin-bottom:14px; text-align:left; }
input { width:100%; padding:10px 18px; border:1.5px solid #b2dfdb;
        border-radius:24px; font-size:.95rem; outline:none; }
input:focus { border-color:#7B1FA2; }
.btn { display:block; width:100%; padding:11px; border-radius:24px;
       font-weight:bold; font-size:1rem; border:none; cursor:pointer;
       text-decoration:none; margin-top:8px; }
.btn-primary { background:#00BFA5; color:#fff; }
.btn-gray    { background:#e0f7f4; color:#546E7A; margin-top:12px; }
.btn:hover { opacity:.88; }
.error { background:#FFEBEE; color:#C62828; padding:10px 16px;
         border-radius:12px; font-size:.88rem; margin-bottom:16px; }
.link { color:#7B1FA2; font-size:.9rem; margin-top:16px; display:block; }
</style>
</head>
<body>
<div class="card">
  <h2>Вход в личный кабинет</h2>
  {% if error %}
    <div class="error">{{ error }}</div>
  {% endif %}
  <form method="post" action="{{ url_for('pharmacy.login_post') }}">
    {{ form.hidden_tag() }}
    <div class="form-group">
      {{ form.login(placeholder="Логин...", required=True, autofocus=True) }}
    </div>
    <div class="form-group">
      {{ form.password(placeholder="Пароль...", required=True) }}
    </div>
    <button class="btn btn-primary" type="submit">ВХОД</button>
  </form>
  <span style="color:#90A4AE;font-size:.88rem;margin-top:14px;display:block;">
    Нет личного кабинета?
  </span>
  <a class="link" href="{{ url_for('pharmacy.register') }}">Регистрация</a>
  <a class="btn btn-gray" href="{{ url_for('pharmacy.products') }}">Назад</a>
</div>
</body>
</html>
