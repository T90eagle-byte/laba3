{% extends "base.tpl" %}
{% block content %}
{% if false %}
<h1>{{ "Редактирование пользователя" if it.id else "Новый пользователь" }}</h1>
{% if error %}
  <div class="error-box">{{ error }}</div>
{% endif %}
<div class="form-card" style="max-width:540px;">
  <form action="{{ module_url('admin_user_save') }}" method="post">
    {{ form.hidden_tag() }}
    {{ form.id(value=it.id) }}

    <div class="form-group">
      <label>Фамилия</label>
      {{ form.surname(value=it.surname) }}
    </div>
    <div class="form-group">
      <label>Имя</label>
      {{ form.name(value=it.name) }}
    </div>
    <div class="form-group">
      <label>Отчество</label>
      {{ form.patronymic(value=it.patronymic) }}
    </div>
    <div class="form-group">
      <label>Логин</label>
      {{ form.login(value=it.login, required=True) }}
    </div>
    <div class="form-group">
      <label>Пароль</label>
      {{ form.password(placeholder="оставьте пустым без изменения") }}
    </div>
    <div class="form-group">
      <label>Подтверждение пароля</label>
      {{ form.confirm(placeholder="повторите пароль") }}
    </div>
    <div class="form-group">
      <label>Адрес доставки</label>
      {{ form.address(value=it.address) }}
    </div>
    <div class="form-group">
      <label>Роль</label>
      {{ form.is_admin() }}
    </div>

    <div class="form-actions">
      <button class="btn btn-primary" type="submit">Сохранить</button>
      <a class="btn btn-gray" href="{{ module_url('admin') }}">Назад</a>
    </div>
  </form>
</div>
{% endif %}

<section class="admin-lite-form-page" aria-label="Форма пользователя">
  <header class="admin-lite-form-header">
    <h1 class="admin-lite-form-title">{{ "Редактирование пользователя" if it.id else "Новый пользователь" }}</h1>
    <a class="btn btn-gray" href="{{ module_url('admin') }}">Назад</a>
  </header>

  {% if error %}
    <div class="error-box admin-lite-error">{{ error }}</div>
  {% endif %}

  <div class="form-card admin-lite-form-card">
    <form class="admin-lite-form-grid" action="{{ module_url('admin_user_save') }}" method="post">
      {{ form.hidden_tag() }}
      {{ form.id(value=it.id) }}

      <div class="form-group admin-lite-form-group">
        <label for="{{ form.surname.id }}">Фамилия</label>
        {{ form.surname(value=it.surname) }}
      </div>
      <div class="form-group admin-lite-form-group">
        <label for="{{ form.name.id }}">Имя</label>
        {{ form.name(value=it.name) }}
      </div>
      <div class="form-group admin-lite-form-group">
        <label for="{{ form.patronymic.id }}">Отчество</label>
        {{ form.patronymic(value=it.patronymic) }}
      </div>
      <div class="form-group admin-lite-form-group">
        <label for="{{ form.login.id }}">Логин</label>
        {{ form.login(value=it.login, required=True) }}
      </div>
      <div class="form-group admin-lite-form-group">
        <label for="{{ form.password.id }}">Пароль</label>
        {{ form.password(placeholder="оставьте пустым без изменения") }}
      </div>
      <div class="form-group admin-lite-form-group">
        <label for="{{ form.confirm.id }}">Подтверждение пароля</label>
        {{ form.confirm(placeholder="повторите пароль") }}
      </div>
      <div class="form-group admin-lite-form-group">
        <label for="{{ form.address.id }}">Адрес доставки</label>
        {{ form.address(value=it.address) }}
      </div>
      <div class="form-group admin-lite-form-group">
        <label for="{{ form.is_admin.id }}">Роль</label>
        {{ form.is_admin() }}
      </div>

      <div class="form-actions admin-lite-form-actions">
        <button class="btn btn-primary" type="submit">Сохранить</button>
        <a class="btn btn-gray" href="{{ module_url('admin') }}">Назад</a>
      </div>
    </form>
  </div>
</section>
{% endblock %}
