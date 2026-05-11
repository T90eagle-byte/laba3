{% extends "base.tpl" %}
{% block content %}
<h1>Импорт данных из ЛР2</h1>
<p style="color:#546E7A;margin-bottom:20px;">
  Файл: <code>{{ path }}</code>
</p>
<div class="info-box">{{ msg }}</div>
<div style="display:flex;gap:12px;">
  <a class="btn btn-primary" href="{{ module_url('admin') }}">Админка</a>
  <a class="btn btn-gray" href="{{ module_url('products') }}">Каталог</a>
</div>
{% endblock %}
