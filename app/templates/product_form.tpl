{% extends "base.tpl" %}
{% block content %}
<h1>{{ "Редактирование товара" if it.id else "Новый товар" }}</h1>
<div class="form-card">
  <form action="{{ module_url('product_add') }}" method="post">
    {{ form.hidden_tag() }}
    {{ form.id(value=it.id) }}
    <div class="form-group">
      <label>Название</label>
      {{ form.name(value=it.name, required=True) }}
    </div>
    <div class="form-group">
      <label>Дозировка</label>
      {{ form.dosage(value=it.dosage, placeholder="например: 500") }}
    </div>
    <div class="form-group">
      <label>Цена (руб.)</label>
      {{ form.price(value=it.price, min="0", step="0.01", required=True) }}
    </div>
    <div class="form-group">
      <label>Наличие</label>
      {{ form.in_stock() }}
    </div>
    <div class="form-actions">
      <button class="btn btn-primary" type="submit">Сохранить</button>
      <a class="btn btn-gray" href="{{ module_url('admin') }}">Назад</a>
    </div>
  </form>
</div>
{% endblock %}
