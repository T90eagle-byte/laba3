{% extends "base.tpl" %}
{% block content %}
<h1>{{ "Редактирование товара" if it.id else "Новый товар" }}</h1>
<div class="form-card">
  <form action="{{ url_for('pharmacy.product_add') }}" method="post">
    <input type="hidden" name="id" value="{{ it.id }}">
    <div class="form-group">
      <label>Название</label>
      <input type="text" name="name" value="{{ it.name }}" required>
    </div>
    <div class="form-group">
      <label>Дозировка</label>
      <input type="text" name="dosage" value="{{ it.dosage }}">
    </div>
    <div class="form-group">
      <label>Цена (руб.)</label>
      <input type="number" name="price" value="{{ it.price }}" min="0" step="0.01" required>
    </div>
    <div class="form-group">
      <label>Наличие</label>
      <select name="in_stock">
        <option value="1" {{ "selected" if it.in_stock }}>Есть в наличии</option>
        <option value="0" {{ "selected" if not it.in_stock }}>Нет в наличии</option>
      </select>
    </div>
    <div class="form-actions">
      <button class="btn btn-primary" type="submit">Сохранить</button>
      <a class="btn btn-gray" href="{{ url_for('pharmacy.products') }}">Назад</a>
    </div>
  </form>
</div>
{% endblock %}
