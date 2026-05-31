<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Регистрация — Invalidhelp</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='css/app.css') }}">
</head>
<body class="auth-page auth-page-register">
  <main class="auth-shell auth-shell-register">
    <a class="auth-back" href="{{ module_url('login') }}">
      <span class="auth-back-icon auth-back-icon-register" aria-hidden="true"></span>
      <span class="auth-back-text">Назад</span>
    </a>

    <section class="auth-screen auth-screen-register">
      <h1 class="auth-title auth-title-register">Регистрация</h1>

      {% if error %}
        <div class="error-box auth-error">{{ error }}</div>
      {% endif %}

      <form class="auth-form auth-form-register" method="post" action="{{ module_url('register_post') }}">
        {{ form.hidden_tag() }}

        <div class="auth-register-grid">
          <div class="auth-field auth-field-register">
            <label class="auth-label" for="{{ form.name.id }}">Имя:</label>
            {{ form.name(class_='auth-input auth-input-register', placeholder='...') }}
          </div>

          <div class="auth-field auth-field-register">
            <label class="auth-label" for="{{ form.password.id }}">Пароль:</label>
            {{ form.password(class_='auth-input auth-input-register', placeholder='...', required=True) }}
          </div>

          <div class="auth-field auth-field-register">
            <label class="auth-label" for="{{ form.surname.id }}">Фамилия:</label>
            {{ form.surname(class_='auth-input auth-input-register', placeholder='...') }}
          </div>

          <div class="auth-field auth-field-register">
            <label class="auth-label" for="{{ form.confirm.id }}">Подтвердите пароль:</label>
            {{ form.confirm(class_='auth-input auth-input-register', placeholder='...', required=True) }}
          </div>

          <div class="auth-field auth-field-register">
            <label class="auth-label" for="{{ form.patronymic.id }}">Отчество:</label>
            {{ form.patronymic(class_='auth-input auth-input-register', placeholder='...') }}
          </div>

          <div class="auth-field auth-field-register">
            <label class="auth-label" for="{{ form.address.id }}">Адрес доставки:</label>
            {{ form.address(class_='auth-input auth-input-register', placeholder='...') }}
          </div>

          <div class="auth-field auth-field-register auth-field-login-register">
            <label class="auth-label" for="{{ form.login.id }}">Логин:</label>
            {{ form.login(class_='auth-input auth-input-register', placeholder='...', required=True) }}
          </div>
        </div>

        <div class="auth-register-actions">
          <button class="auth-submit auth-submit-register" type="submit">Зарегистрироваться</button>
        </div>
      </form>
    </section>
  </main>
</body>
</html>
