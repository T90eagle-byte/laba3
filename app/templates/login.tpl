<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Вход — Invalidhelp</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='css/app.css') }}">
</head>
<body class="auth-page auth-page-login">
  <main class="auth-shell auth-shell-login">
    <a class="auth-back" href="{{ module_url('products') }}">
      <span class="auth-back-icon auth-back-icon-login" aria-hidden="true"></span>
      <span class="auth-back-text">Назад</span>
    </a>

    <section class="auth-screen auth-screen-login">
      <h1 class="auth-title auth-title-login">Вход в личный кабинет</h1>

      {% if error %}
        <div class="error-box auth-error">{{ error }}</div>
      {% endif %}

      <form class="auth-form auth-form-login" method="post" action="{{ module_url('login_post') }}">
        {{ form.hidden_tag() }}
        <div class="auth-field auth-field-login">
          {{ form.login(class_='auth-input auth-input-login', placeholder='Логин...', required=True, autofocus=True) }}
        </div>
        <div class="auth-field auth-field-login">
          {{ form.password(class_='auth-input auth-input-login', placeholder='Пароль...', required=True) }}
        </div>

        <div class="auth-login-footer">
          <div class="auth-login-signup">
            <p class="auth-login-signup-text">Нет личного кабинета?</p>
            <a class="auth-login-signup-link" href="{{ module_url('register') }}">Регистрация</a>
          </div>
          <button class="auth-submit auth-submit-login" type="submit">Вход</button>
        </div>
      </form>
    </section>
  </main>
</body>
</html>
