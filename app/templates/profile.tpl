{% extends "base.tpl" %}
{% block content %}
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
      <a class="btn btn-danger" href="{{ module_url('logout') }}">ВЫЙТИ</a>
    </div>
  </form>
</div>
{% endblock %}
