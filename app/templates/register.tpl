<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Регистрация — Invalidhelp</title>
<style>
* { box-sizing:border-box; margin:0; padding:0; }
body { font-family:Arial,sans-serif; background:#e0f7f4;
       display:flex; align-items:center; justify-content:center;
       min-height:100vh; padding:24px; }
.card { background:#fff; border-radius:20px; padding:40px 48px;
        width:100%; max-width:420px; box-shadow:0 4px 20px #0001; text-align:center; }
h2 { color:#37474F; margin-bottom:24px; font-size:1.2rem; }
.form-group { margin-bottom:12px; text-align:left; }
input { width:100%; padding:10px 18px; border:1.5px solid #b2dfdb;
        border-radius:24px; font-size:.93rem; outline:none; }
input:focus { border-color:#7B1FA2; }
.btn { display:block; width:100%; padding:11px; border-radius:24px;
       font-weight:bold; font-size:1rem; border:none; cursor:pointer;
       text-decoration:none; margin-top:10px; }
.btn-primary { background:#00BFA5; color:#fff; }
.btn-gray    { background:#e0f7f4; color:#546E7A; }
.btn:hover { opacity:.88; }
.error { background:#FFEBEE; color:#C62828; padding:10px 16px;
         border-radius:12px; font-size:.88rem; margin-bottom:14px; }
</style>
</head>
<body>
<div class="card">
  <h2>Регистрация</h2>
  {% if error %}
    <div class="error">{{ error }}</div>
  {% endif %}
  <form method="post" action="{{ url_for('pharmacy.register_post') }}">
    {{ form.hidden_tag() }}
    <div class="form-group">
      {{ form.surname(placeholder="Фамилия...") }}
    </div>
    <div class="form-group">
      {{ form.name(placeholder="Имя...") }}
    </div>
    <div class="form-group">
      {{ form.patronymic(placeholder="Отчество...") }}
    </div>
    <div class="form-group">
      {{ form.login(placeholder="Логин...", required=True) }}
    </div>
    <div class="form-group">
      {{ form.password(placeholder="Пароль...", required=True) }}
    </div>
    <div class="form-group">
      {{ form.confirm(placeholder="Подтвердите пароль...", required=True) }}
    </div>
    <div class="form-group">
      {{ form.address(placeholder="Адрес доставки...") }}
    </div>
    <button class="btn btn-primary" type="submit">Зарегистрироваться</button>
  </form>
  <a class="btn btn-gray" href="{{ url_for('pharmacy.login') }}" style="margin-top:10px;">Назад</a>
</div>
</body>
</html>
