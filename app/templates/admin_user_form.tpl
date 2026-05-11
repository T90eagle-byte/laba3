{% extends "base.tpl" %}
{% block content %}
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
{% endblock %}
