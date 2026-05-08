{% extends "base.tpl" %}
{% block content %}
<h1>Настройки профиля</h1>
<div class="form-card" style="max-width:540px;">
  <form action="{{ url_for('pharmacy.profile_save') }}" method="post">
    <input type="hidden" name="id" value="{{ it.id }}">

    <h2 style="margin-bottom:16px;">Личные данные</h2>
    <div class="form-group">
      <label>Имя</label>
      <input type="text" name="name" value="{{ it.name }}">
    </div>
    <div class="form-group">
      <label>Фамилия</label>
      <input type="text" name="surname" value="{{ it.surname }}">
    </div>
    <div class="form-group">
      <label>Отчество</label>
      <input type="text" name="patronymic" value="{{ it.patronymic }}">
    </div>
    <div class="form-group">
      <label>Логин</label>
      <input type="text" name="login" value="{{ it.login }}">
    </div>
    <div class="form-group">
      <label>Адрес доставки</label>
      <input type="text" name="address" value="{{ it.address }}">
    </div>

    <hr style="border:none;border-top:1px solid #e0f7f4;margin:20px 0;">
    <h2 style="margin-bottom:16px;">Смена пароля</h2>
    <div class="form-group">
      <label>Текущий пароль</label>
      <input type="password" name="current_password" placeholder="...">
    </div>
    <div class="form-group">
      <label>Новый пароль</label>
      <input type="password" name="new_password" placeholder="...">
    </div>
    <div class="form-group">
      <label>Подтвердите пароль</label>
      <input type="password" name="confirm_password" placeholder="...">
    </div>

    <div class="form-actions">
      <button class="btn btn-primary" type="submit">СОХРАНИТЬ</button>
      <a class="btn btn-danger" href="{{ url_for('pharmacy.logout') }}">ВЫЙТИ</a>
    </div>
  </form>
</div>
{% endblock %}
