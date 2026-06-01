{% extends "base.tpl" %}
{% block content %}
{% if false %}
<h1>Настройки профиля</h1>
<div class="form-card" style="max-width:540px;">
  <form action="{{ module_url('profile_save') }}" method="post">
    {{ form.hidden_tag() }}
    {{ form.id(value=it.id) }}

    <h2 style="margin-bottom:16px;">Личные данные</h2>
    <div class="form-group">
      <label>Имя</label>
      {{ form.name(value=it.name) }}
    </div>
    <div class="form-group">
      <label>Фамилия</label>
      {{ form.surname(value=it.surname) }}
    </div>
    <div class="form-group">
      <label>Отчество</label>
      {{ form.patronymic(value=it.patronymic) }}
    </div>
    <div class="form-group">
      <label>Логин</label>
      {{ form.login(value=it.login) }}
    </div>
    <div class="form-group">
      <label>Адрес доставки</label>
      {{ form.address(value=it.address) }}
    </div>

    <hr style="border:none;border-top:1px solid #e0f7f4;margin:20px 0;">
    <h2 style="margin-bottom:16px;">Смена пароля</h2>
    <div class="form-group">
      <label>Текущий пароль</label>
      {{ form.current_password(placeholder="...") }}
    </div>
    <div class="form-group">
      <label>Новый пароль</label>
      {{ form.new_password(placeholder="...") }}
    </div>
    <div class="form-group">
      <label>Подтвердите пароль</label>
      {{ form.confirm_password(placeholder="...") }}
    </div>

    <div class="form-actions">
      <button class="btn btn-primary" type="submit">СОХРАНИТЬ</button>
      {{ action_form.hidden_tag() }}
      <button
        class="btn btn-danger"
        type="submit"
        formaction="{{ module_url('logout') }}"
        formmethod="post"
        formnovalidate
      >
        ВЫЙТИ
      </button>
    </div>
  </form>
</div>
{% endif %}

<section class="profile-d2c-page" aria-label="Настройки профиля">
  <header class="profile-d2c-top">
    <a class="profile-d2c-back-link" href="{{ module_url('my_orders') }}">
      <span class="profile-d2c-back-icon" aria-hidden="true"></span>
      <span>Назад</span>
    </a>
    <h1 class="profile-d2c-title">Настройки профиля</h1>
  </header>

  <div class="profile-d2c-surface">
    <form id="profile-save-form" class="profile-d2c-form" action="{{ module_url('profile_save') }}" method="post">
      {{ form.hidden_tag() }}
      {{ form.id(value=it.id) }}

      <section class="profile-d2c-column" aria-label="Личные данные">
        <div class="profile-d2c-field">
          <label for="{{ form.name.id }}" class="profile-d2c-label">Имя:</label>
          {{ form.name(value=it.name, class_='profile-d2c-input', placeholder='...') }}
          {% if form.name.errors %}
            <ul class="profile-d2c-errors">
              {% for error in form.name.errors %}
                <li>{{ error }}</li>
              {% endfor %}
            </ul>
          {% endif %}
        </div>

        <div class="profile-d2c-field">
          <label for="{{ form.surname.id }}" class="profile-d2c-label">Фамилия:</label>
          {{ form.surname(value=it.surname, class_='profile-d2c-input', placeholder='...') }}
          {% if form.surname.errors %}
            <ul class="profile-d2c-errors">
              {% for error in form.surname.errors %}
                <li>{{ error }}</li>
              {% endfor %}
            </ul>
          {% endif %}
        </div>

        <div class="profile-d2c-field">
          <label for="{{ form.patronymic.id }}" class="profile-d2c-label">Отчество:</label>
          {{ form.patronymic(value=it.patronymic, class_='profile-d2c-input', placeholder='...') }}
          {% if form.patronymic.errors %}
            <ul class="profile-d2c-errors">
              {% for error in form.patronymic.errors %}
                <li>{{ error }}</li>
              {% endfor %}
            </ul>
          {% endif %}
        </div>

        <div class="profile-d2c-field">
          <label for="{{ form.login.id }}" class="profile-d2c-label">Логин:</label>
          {{ form.login(value=it.login, class_='profile-d2c-input', placeholder='...') }}
          {% if form.login.errors %}
            <ul class="profile-d2c-errors">
              {% for error in form.login.errors %}
                <li>{{ error }}</li>
              {% endfor %}
            </ul>
          {% endif %}
        </div>
      </section>

      <section class="profile-d2c-column" aria-label="Безопасность и доставка">
        <div class="profile-d2c-field">
          <label for="{{ form.current_password.id }}" class="profile-d2c-label">Текущий пароль:</label>
          {{ form.current_password(class_='profile-d2c-input', placeholder='...') }}
          {% if form.current_password.errors %}
            <ul class="profile-d2c-errors">
              {% for error in form.current_password.errors %}
                <li>{{ error }}</li>
              {% endfor %}
            </ul>
          {% endif %}
        </div>

        <div class="profile-d2c-field">
          <label for="{{ form.new_password.id }}" class="profile-d2c-label">Новый пароль:</label>
          {{ form.new_password(class_='profile-d2c-input', placeholder='...') }}
          {% if form.new_password.errors %}
            <ul class="profile-d2c-errors">
              {% for error in form.new_password.errors %}
                <li>{{ error }}</li>
              {% endfor %}
            </ul>
          {% endif %}
        </div>

        <div class="profile-d2c-field">
          <label for="{{ form.confirm_password.id }}" class="profile-d2c-label">Подтвердите пароль:</label>
          {{ form.confirm_password(class_='profile-d2c-input', placeholder='...') }}
          {% if form.confirm_password.errors %}
            <ul class="profile-d2c-errors">
              {% for error in form.confirm_password.errors %}
                <li>{{ error }}</li>
              {% endfor %}
            </ul>
          {% endif %}
        </div>

        <div class="profile-d2c-field">
          <label for="{{ form.address.id }}" class="profile-d2c-label">Адрес доставки:</label>
          {{ form.address(value=it.address, class_='profile-d2c-input', placeholder='...') }}
          {% if form.address.errors %}
            <ul class="profile-d2c-errors">
              {% for error in form.address.errors %}
                <li>{{ error }}</li>
              {% endfor %}
            </ul>
          {% endif %}
        </div>
      </section>
    </form>

    <form id="profile-logout-form" class="profile-d2c-logout-form" action="{{ module_url('logout') }}" method="post">
      {{ action_form.hidden_tag() }}
    </form>

    <div class="profile-d2c-actions">
      <button class="profile-d2c-save-btn" type="submit" form="profile-save-form">СОХРАНИТЬ</button>
      <button class="profile-d2c-logout-btn" type="submit" form="profile-logout-form">ВЫЙТИ</button>
    </div>
  </div>
</section>
{% endblock %}
