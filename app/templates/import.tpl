{% extends "base.tpl" %}
{% block content %}
{% if false %}
<h1>Импорт данных из ЛР2</h1>
<p style="color:#546E7A;margin-bottom:20px;">
  Файл: <code>{{ path }}</code>
</p>
<div class="info-box">{{ msg }}</div>
<div style="display:flex;gap:12px;">
  <a class="btn btn-primary" href="{{ module_url('admin') }}">Админка</a>
  <a class="btn btn-gray" href="{{ module_url('products') }}">Каталог</a>
</div>
{% endif %}

<section class="admin-lite-import-page" aria-label="Импорт">
  <header class="admin-lite-form-header">
    <h1 class="admin-lite-form-title">Импорт данных из ЛР2</h1>
  </header>

  <div class="admin-lite-import-card">
    <p class="admin-lite-import-path">Файл: <code>{{ path }}</code></p>
    <div class="info-box admin-lite-import-message">{{ msg }}</div>
    <div class="admin-lite-import-actions">
      <a class="btn btn-primary" href="{{ module_url('admin') }}">Админка</a>
      <a class="btn btn-gray" href="{{ module_url('products') }}">Каталог</a>
    </div>
  </div>
</section>
{% endblock %}
