# -*- coding: utf-8 -*-
import os, sqlite3, pickle, datetime, hashlib, hmac
from dataclasses import dataclass, field
from functools import wraps
from flask import (Blueprint, render_template, request, redirect, session, flash,
                   url_for, g, abort)
from flask_login import (
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.forms import (
    ActionForm,
    AdminUserForm,
    LoginForm,
    OrderForm,
    ProductForm,
    ProfileForm,
    RegisterForm,
)

bp = Blueprint('pharmacy', __name__)

_BASE     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR  = os.path.join(_BASE, 'data')
DB_PATH   = os.path.join(_BASE, 'data', 'pharmacy.sqlite')
PKL_PATH  = os.path.join(_BASE, 'data', 'data.pkl')
CATALOG_PKL_PATH = os.path.join(_BASE, 'data', 'catalog.pkl')
LEGACY_CATALOG_PKL_PATH = os.path.join(
    os.path.dirname(_BASE), 'pharmacy_app', 'pharmacy', 'catalog.pkl')
ADMIN_LOGIN = 'admin'
ADMIN_PASSWORD = 'admin'
MG_UNIT = '\u043c\u0433'
LEGACY_MG_UNITS = ('\u00d0\u00bc\u00d0\u00b3', '\u0420\u0458\u0420\u0456', '\u00ec\u00e3')
PAYMENT_CASH = '\u043d\u0430\u043b\u0438\u0447\u043d\u044b\u0435'
CART_MAX_QUANTITY = 99
DEFAULT_PRODUCT_CATEGORY = '\u041b\u0435\u043a\u0430\u0440\u0441\u0442\u0432\u0430'
PRODUCT_CATEGORIES = (
    DEFAULT_PRODUCT_CATEGORY,
    '\u0412\u0438\u0442\u0430\u043c\u0438\u043d\u044b \u0438 \u0411\u0410\u0414',
    '\u041a\u0440\u0430\u0441\u043e\u0442\u0430',
    '\u0413\u0438\u0433\u0438\u0435\u043d\u0430',
)
IMAGE_CHICKEN = '70b63ef52bb9c8e4a75f3a6c46afb62e8b21d8c3.png'
IMAGE_RICE = '8af2af4ea1fe6457c7dfbeb1d53e527d1ce6b985.png'
IMAGE_BUCKWHEAT = '8cf2c29fefeef2f884c05aa49a43170c2f0f9d92.png'
IMAGE_PLACEHOLDER = 'medicinebottleline.png'
IMAGE_BEAUTY = '02ff7106307a0ebe4e335e44540dd57b2a1f8753.png'
IMAGE_HYGIENE = 'medicinebottleline.png'
DEMO_PRODUCTS = (
    ('\u041a\u0443\u0440\u0438\u043d\u043e\u0431\u043e\u043b', '500 \u043c\u0433', 2000, 1, '\u041b\u0435\u043a\u0430\u0440\u0441\u0442\u0432\u0430'),
    ('\u0420\u0438\u0441\u043e\u0441\u0442\u0430\u043d\u043e\u043d', '250 \u043c\u0433', 1250, 1, '\u041b\u0435\u043a\u0430\u0440\u0441\u0442\u0432\u0430'),
    ('\u0422\u0430\u0431\u043b\u0435\u0442\u043e\u0437\u043e\u043b', '100 \u043c\u0433', 740, 1, '\u041b\u0435\u043a\u0430\u0440\u0441\u0442\u0432\u0430'),
    ('\u0413\u0440\u0435\u0447\u0435\u0441\u0442\u0435\u0440\u043e\u043d', '890 \u043c\u0433', 2000, 1, '\u0412\u0438\u0442\u0430\u043c\u0438\u043d\u044b \u0438 \u0411\u0410\u0414'),
    ('\u0412\u0438\u0442\u0430\u043c\u0438\u043d\u0443\u0441 C', '1000 \u043c\u0433', 560, 1, '\u0412\u0438\u0442\u0430\u043c\u0438\u043d\u044b \u0438 \u0411\u0410\u0414'),
    ('\u041e\u043c\u0435\u0433\u0430\u043d\u043e\u043b', '120 \u043a\u0430\u043f\u0441\u0443\u043b', 980, 1, '\u0412\u0438\u0442\u0430\u043c\u0438\u043d\u044b \u0438 \u0411\u0410\u0414'),
    ('\u041a\u0440\u0435\u043c\u043e\u043b\u0438\u043d', '50 \u043c\u043b', 430, 1, '\u041a\u0440\u0430\u0441\u043e\u0442\u0430'),
    ('\u041c\u0430\u0441\u043a\u043e\u043b\u0430\u0433\u0435\u043d', '30 \u043c\u043b', 890, 1, '\u041a\u0440\u0430\u0441\u043e\u0442\u0430'),
    ('\u0428\u0430\u043c\u043f\u0443\u043d\u043e\u043b', '250 \u043c\u043b', 360, 1, '\u041a\u0440\u0430\u0441\u043e\u0442\u0430'),
    ('\u0417\u0443\u0431\u0430\u0441\u0442\u0438\u043d', '100 \u043c\u043b', 220, 1, '\u0413\u0438\u0433\u0438\u0435\u043d\u0430'),
    ('\u041c\u044b\u043b\u043e\u0434\u0435\u0440\u043c', '90 \u0433', 150, 1, '\u0413\u0438\u0433\u0438\u0435\u043d\u0430'),
    ('\u0421\u0430\u043d\u0438\u0442\u0430\u0439\u0437\u0435\u0440\u043e\u043b', '100 \u043c\u043b', 190, 1, '\u0413\u0438\u0433\u0438\u0435\u043d\u0430'),
)


# ─────────────────────────────────────────────────────────────────
#  Утилита хэширования
# ─────────────────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    return generate_password_hash(password)


def hash_password_legacy(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def _is_legacy_sha256_hash(value: str) -> bool:
    if not isinstance(value, str) or len(value) != 64:
        return False
    return all(ch in '0123456789abcdef' for ch in value.lower())


def verify_password(stored_hash: str, password: str):
    if not stored_hash:
        return False, False

    try:
        if check_password_hash(stored_hash, password):
            return True, False
    except (ValueError, TypeError):
        pass

    if _is_legacy_sha256_hash(stored_hash):
        legacy_hash = hash_password_legacy(password)
        if hmac.compare_digest(stored_hash, legacy_hash):
            return True, True

    return False, False


def normalize_dosage(dosage: str) -> str:
    value = (dosage or '').strip()
    if not value:
        return ''
    lower = value.lower().replace('.', '')
    for suffix in (MG_UNIT, *LEGACY_MG_UNITS):
        if lower.endswith(suffix.lower()):
            value = value[:-len(suffix)].strip().rstrip(',').strip()
            break
    return f"{value}, {MG_UNIT}" if value else MG_UNIT


def normalize_category(category: str) -> str:
    value = (category or '').strip()
    return value if value in PRODUCT_CATEGORIES else DEFAULT_PRODUCT_CATEGORY


def product_image_filename(product=None, *, name: str = '', category: str = '') -> str:
    if product is not None:
        if isinstance(product, dict):
            name = product.get('name', name)
            category = product.get('category', category)
        else:
            name = getattr(product, 'name', name)
            category = getattr(product, 'category', category)

    name_key = (name or '').strip().lower()
    category_name = normalize_category(category)

    if 'кур' in name_key:
        return IMAGE_CHICKEN
    if 'греч' in name_key:
        return IMAGE_BUCKWHEAT
    if 'рисост' in name_key or 'рисостан' in name_key:
        return IMAGE_RICE
    if 'витаминус c' in name_key:
        return IMAGE_RICE
    if 'омеганол' in name_key:
        return IMAGE_BUCKWHEAT

    if category_name == '\u041a\u0440\u0430\u0441\u043e\u0442\u0430':
        return IMAGE_BEAUTY
    if category_name == '\u0413\u0438\u0433\u0438\u0435\u043d\u0430':
        return IMAGE_HYGIENE
    if category_name == '\u0412\u0438\u0442\u0430\u043c\u0438\u043d\u044b \u0438 \u0411\u0410\u0414':
        return IMAGE_BUCKWHEAT
    if category_name == DEFAULT_PRODUCT_CATEGORY:
        return IMAGE_PLACEHOLDER
    return IMAGE_PLACEHOLDER


def get_import_path() -> str:
    for path in (PKL_PATH, CATALOG_PKL_PATH, LEGACY_CATALOG_PKL_PATH):
        if os.path.exists(path):
            return path
    return PKL_PATH


def module_endpoint(endpoint: str) -> str:
    return f"{bp.name}.{endpoint}"


def module_url(endpoint: str, **values):
    return url_for(module_endpoint(endpoint), **values)


@bp.app_context_processor
def inject_module_url():
    return {
        'module_url': module_url,
        'cart_count': get_cart_count,
        'product_image': product_image_filename,
        'action_form': ActionForm(),
    }


def get_cart() -> dict:
    cart = session.get('cart')
    return cart if isinstance(cart, dict) else {}


def save_cart(cart: dict):
    clean_cart = {}
    for product_id, quantity in cart.items():
        clean_quantity = normalize_cart_quantity(quantity)
        if clean_quantity > 0:
            clean_cart[str(product_id)] = clean_quantity
    session['cart'] = clean_cart
    session.modified = True


def get_cart_count() -> int:
    total = 0
    for quantity in get_cart().values():
        total += normalize_cart_quantity(quantity)
    return total


def normalize_cart_quantity(quantity) -> int:
    try:
        value = int(quantity)
    except (TypeError, ValueError):
        return 0
    if value <= 0:
        return 0
    return min(value, CART_MAX_QUANTITY)


def admin_required(view):
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if not getattr(current_user, 'is_admin', 0):
            abort(403)
        return view(*args, **kwargs)
    return wrapped


# ─────────────────────────────────────────────────────────────────
#  Элементы картотеки
# ─────────────────────────────────────────────────────────────────

@dataclass
class UserItem(UserMixin):
    id: int = 0
    name: str = ''
    surname: str = ''
    patronymic: str = ''
    login: str = ''
    password_hash: str = ''
    address: str = ''
    is_admin: int = 0

    def full_name(self):
        return f"{self.surname} {self.name} {self.patronymic}".strip()

    def initials(self):
        parts = [self.surname, self.name]
        return ''.join(p[0].upper() for p in parts if p)

    def get_id(self):
        return str(self.id)

    def __str__(self):
        return self.full_name()

    def DBLoad(self, r):
        self.id            = r['id']
        self.name          = r['name']
        self.surname       = r['surname']
        self.patronymic    = r['patronymic']
        self.login         = r['login']
        self.password_hash = r['password_hash']
        self.address       = r['address']
        self.is_admin      = r['is_admin'] if 'is_admin' in r.keys() else 0

    def DBStore(self, db):
        if not self.id:
            db.execute(
                "INSERT INTO users VALUES(NULL,?,?,?,?,?,?,?)",
                (self.name, self.surname, self.patronymic,
                 self.login, self.password_hash, self.address, self.is_admin)
            )
        else:
            db.execute(
                "UPDATE users SET name=?,surname=?,patronymic=?,"
                "login=?,address=?,is_admin=? WHERE id=?",
                (self.name, self.surname, self.patronymic,
                 self.login, self.address, self.is_admin, self.id)
            )

    def Input(self, io):
        self.id         = int(io.Input('id') or 0)
        self.name       = io.Input('name') or ''
        self.surname    = io.Input('surname') or ''
        self.patronymic = io.Input('patronymic') or ''
        self.login      = io.Input('login') or ''
        self.address    = io.Input('address') or ''

    def Output(self, io):
        return io.OutputProfile(self)


@dataclass
class ProductItem:
    id: int = 0
    name: str = ''
    dosage: str = ''
    category: str = DEFAULT_PRODUCT_CATEGORY
    price: float = 0.0
    in_stock: int = 1

    def __str__(self):
        return f"{self.name} {self.dosage} — {self.price:.0f} руб."

    def DBLoad(self, r):
        self.id       = r['id']
        self.name     = r['name']
        self.dosage   = normalize_dosage(r['dosage'])
        self.category = normalize_category(
            r['category'] if 'category' in r.keys() else DEFAULT_PRODUCT_CATEGORY
        )
        self.price    = r['price']
        self.in_stock = r['in_stock']

    def DBStore(self, db):
        if not self.id:
            db.execute(
                "INSERT INTO products(name,dosage,price,in_stock,category) VALUES(?,?,?,?,?)",
                (
                    self.name,
                    normalize_dosage(self.dosage),
                    self.price,
                    self.in_stock,
                    normalize_category(self.category),
                )
            )
        else:
            db.execute(
                "UPDATE products SET name=?,dosage=?,price=?,in_stock=?,category=? WHERE id=?",
                (
                    self.name,
                    normalize_dosage(self.dosage),
                    self.price,
                    self.in_stock,
                    normalize_category(self.category),
                    self.id,
                )
            )

    def Input(self, io):
        self.id       = int(io.Input('id') or 0)
        self.name     = io.Input('name') or ''
        self.dosage   = normalize_dosage(io.Input('dosage') or '')
        self.category = normalize_category(io.Input('category') or DEFAULT_PRODUCT_CATEGORY)
        self.price    = float(io.Input('price') or 0)
        self.in_stock = int(io.Input('in_stock') or 1)

    def Output(self, io):
        return io.OutputProduct(self)


@dataclass
class OrderItem:
    id: int = 0
    user_id: int = 0
    payment: str = PAYMENT_CASH
    created: datetime.datetime = field(default_factory=datetime.datetime.now)
    items: list = field(default_factory=list)

    def total(self):
        return sum(i['price'] for i in self.items)

    def __str__(self):
        return f"Заказ #{self.id} | {self.total():.0f} руб. | {self.payment}"

    def DBLoad(self, r, dbc):
        self.id      = r['id']
        self.user_id = r['user_id']
        self.payment = r['payment'] or PAYMENT_CASH
        self.created = r['created']
        dbc.execute("SELECT * FROM order_items WHERE order_id=?", (self.id,))
        self.items = [
            {'name': i['product_name'],
             'dosage': i['product_dosage'],
             'price': i['price']}
            for i in dbc.fetchall()
        ]

    def DBStore(self, db):
        if not self.id:
            db.execute(
                "INSERT INTO orders VALUES(NULL,?,?,?)",
                (self.user_id, self.payment, self.created)
            )
            self.id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        else:
            db.execute(
                "UPDATE orders SET payment=? WHERE id=?",
                (self.payment, self.id)
            )
            db.execute("DELETE FROM order_items WHERE order_id=?", (self.id,))

        for it in self.items:
            db.execute(
                "INSERT INTO order_items VALUES(NULL,?,?,?,?)",
                (self.id, it['name'], normalize_dosage(it['dosage']), it['price'])
            )

    def Input(self, io):
        self.id      = int(io.Input('id') or 0)
        self.user_id = int(io.Input('user_id') or 0)
        self.payment = PAYMENT_CASH
        product_ids  = io.InputList('product_ids')
        storage = get_pharmacy().storage
        self.items = []
        for pid in product_ids:
            p = storage.GetProduct(int(pid))
            if p.id and p.in_stock:
                self.items.append({
                    'name': p.name, 'dosage': normalize_dosage(p.dosage), 'price': p.price
                })

    def Output(self, io):
        return io.OutputOrder(self)


# ─────────────────────────────────────────────────────────────────
#  Стратегия ввода/вывода
# ─────────────────────────────────────────────────────────────────

class FlaskInputOutput:
    def __init__(self, req):
        self.form = req.form

    def Input(self, field):
        return self.form.get(field)

    def InputList(self, field):
        return self.form.getlist(field)

    def OutputProfile(self, item):
        return render_template('profile.tpl', it=item, form=ProfileForm(obj=item))

    def OutputProduct(self, item):
        return render_template('product_form.tpl', it=item, form=ProductForm(obj=item))

    def OutputOrder(self, item):
        products = list(get_pharmacy().storage.GetProducts())
        form = OrderForm(obj=item)
        form.product_ids.choices = [(p.id, f'{p.name} {p.dosage}') for p in products]
        return render_template('order_form.tpl', it=item, products=products, form=form)


# ─────────────────────────────────────────────────────────────────
#  Хранилище
# ─────────────────────────────────────────────────────────────────

class DBStorage:
    def __init__(self):
        self.Load()

    def Load(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        self.db = sqlite3.connect(
            DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT, surname TEXT, patronymic TEXT,
                login TEXT UNIQUE, password_hash TEXT, address TEXT,
                is_admin INTEGER DEFAULT 0)""")
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS products(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT, dosage TEXT, price REAL, in_stock INTEGER,
                category TEXT NOT NULL DEFAULT 'Лекарства')""")
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS orders(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER, payment TEXT, created TIMESTAMP)""")
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS order_items(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER, product_name TEXT,
                product_dosage TEXT, price REAL)""")
        self._migrate()
        self._backfill_product_categories()
        self._ensure_demo_products()
        self._ensure_default_admin()
        self.db.commit()
        self.db.row_factory = sqlite3.Row
        self.dbc = self.db.cursor()

    def _migrate(self):
        columns = [row[1] for row in self.db.execute("PRAGMA table_info(users)").fetchall()]
        if 'is_admin' not in columns:
            self.db.execute("ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0")
        product_columns = [
            row[1] for row in self.db.execute("PRAGMA table_info(products)").fetchall()
        ]
        if 'category' not in product_columns:
            self.db.execute(
                "ALTER TABLE products ADD COLUMN category TEXT NOT NULL DEFAULT 'Лекарства'"
            )

    def _backfill_product_categories(self):
        rules = (
            ('%куринобол%', 'Лекарства'),
            ('%рисост%', 'Лекарства'),
            ('%гречестерон%', 'Витамины и БАД'),
        )
        for pattern, category in rules:
            self.db.execute(
                "UPDATE products SET category=? WHERE lower(name) LIKE ?",
                (category, pattern),
            )
        self.db.execute(
            "UPDATE products SET category=? WHERE category IS NULL OR trim(category)=''",
            (DEFAULT_PRODUCT_CATEGORY,),
        )

    def _ensure_demo_products(self):
        for name, dosage, price, in_stock, category in DEMO_PRODUCTS:
            normalized_dosage = normalize_dosage(dosage)
            self.db.execute(
                "UPDATE products SET category=? "
                "WHERE lower(name)=lower(?) AND dosage=?",
                (normalize_category(category), name, normalized_dosage),
            )
            exists = self.db.execute(
                "SELECT id FROM products WHERE lower(name)=lower(?) AND dosage=?",
                (name, normalized_dosage),
            ).fetchone()
            if exists:
                continue
            self.db.execute(
                "INSERT INTO products(name,dosage,price,in_stock,category) VALUES(?,?,?,?,?)",
                (name, normalized_dosage, float(price), int(in_stock), normalize_category(category)),
            )

    def _ensure_default_admin(self):
        admin_count = self.db.execute(
            "SELECT COUNT(*) FROM users WHERE is_admin=1").fetchone()[0]
        if admin_count:
            return
        existing = self.db.execute(
            "SELECT id FROM users WHERE login=?", (ADMIN_LOGIN,)).fetchone()
        if existing:
            self.db.execute(
                "UPDATE users SET is_admin=1 WHERE id=?", (existing[0],))
            return
        self.db.execute(
            "INSERT INTO users VALUES(NULL,?,?,?,?,?,?,?)",
            ('Admin', '', '', ADMIN_LOGIN, hash_password(ADMIN_PASSWORD), '', 1)
        )

    def Store(self):
        self.db.commit()
        self.db.close()

    # --- Auth ---
    def GetUserByLogin(self, login):
        self.dbc.execute("SELECT * FROM users WHERE login=?", (login,))
        r = self.dbc.fetchone()
        if r:
            u = UserItem()
            u.DBLoad(r)
            return u
        return None

    def LoginExists(self, login, exclude_id=0):
        self.dbc.execute(
            "SELECT id FROM users WHERE login=? AND id<>?",
            (login, exclude_id))
        return self.dbc.fetchone() is not None

    def RegisterUser(self, item):
        item.DBStore(self.db)

    # --- Users ---
    def GetUser(self, id):
        item = UserItem()
        if id > 0:
            self.dbc.execute("SELECT * FROM users WHERE id=?", (id,))
            r = self.dbc.fetchone()
            if r:
                item.DBLoad(r)
        return item

    def GetUsers(self):
        self.dbc.execute("SELECT * FROM users ORDER BY surname")
        for r in self.dbc:
            u = UserItem()
            u.DBLoad(r)
            yield u

    def UpdateUser(self, item):
        item.DBStore(self.db)

    def UpdatePassword(self, user_id, new_hash):
        self.db.execute(
            "UPDATE users SET password_hash=? WHERE id=?",
            (new_hash, user_id))

    def DeleteUser(self, id):
        self.db.execute(
            "DELETE FROM order_items WHERE order_id IN "
            "(SELECT id FROM orders WHERE user_id=?)", (id,))
        self.db.execute("DELETE FROM orders WHERE user_id=?", (id,))
        self.db.execute("DELETE FROM users WHERE id=?", (id,))

    # --- Products ---
    def GetProduct(self, id):
        item = ProductItem()
        if id > 0:
            self.dbc.execute("SELECT * FROM products WHERE id=?", (id,))
            r = self.dbc.fetchone()
            if r:
                item.DBLoad(r)
        return item

    def GetProducts(self, query: str = '', category: str = 'Все'):
        q = (query or '').strip()
        selected_category = (category or '').strip()
        if selected_category == 'Все':
            selected_category = ''
        if selected_category and selected_category not in PRODUCT_CATEGORIES:
            selected_category = ''

        where_clauses = []
        params = []
        if q:
            # SQLite LIKE does not reliably fold Cyrillic case, so we check
            # several safe variants while keeping parameterized placeholders.
            q_title = f"{q[:1].upper()}{q[1:]}" if q else q
            patterns = [f"%{q}%", f"%{q_title}%", f"%{q.upper()}%"]
            where_clauses.append(
                "(name LIKE ? OR name LIKE ? OR name LIKE ? "
                "OR dosage LIKE ? OR dosage LIKE ? OR dosage LIKE ?)"
            )
            params.extend((*patterns, *patterns))
        if selected_category:
            where_clauses.append("category=?")
            params.append(selected_category)

        sql = "SELECT * FROM products"
        if where_clauses:
            sql += " WHERE " + " AND ".join(where_clauses)
        sql += " ORDER BY name"
        self.dbc.execute(sql, tuple(params))
        for r in self.dbc:
            p = ProductItem()
            p.DBLoad(r)
            yield p

    def AddProduct(self, item):
        item.DBStore(self.db)

    def DeleteProduct(self, id):
        self.db.execute("DELETE FROM products WHERE id=?", (id,))

    # --- Orders ---
    def GetOrder(self, id):
        item = OrderItem()
        if id > 0:
            self.dbc.execute("SELECT * FROM orders WHERE id=?", (id,))
            r = self.dbc.fetchone()
            if r:
                item.DBLoad(r, self.db.cursor())
        return item

    def GetUserOrders(self, user_id):
        self.dbc.execute(
            "SELECT * FROM orders WHERE user_id=? ORDER BY id DESC",
            (user_id,))
        for r in self.dbc.fetchall():
            o = OrderItem()
            o.DBLoad(r, self.db.cursor())
            yield o

    def AddOrder(self, item):
        item.DBStore(self.db)

    def DeleteOrder(self, id):
        self.db.execute("DELETE FROM order_items WHERE order_id=?", (id,))
        self.db.execute("DELETE FROM orders WHERE id=?", (id,))

    # --- Импорт из pickle ЛР2 ---
    def ImportFromPickle(self, path):
        try:
            with open(path, 'rb') as f:
                data = pickle.load(f)
        except Exception as e:
            return f"Ошибка чтения файла: {e}"

        count_u = count_p = 0
        users = data.get('users', []) if isinstance(data, dict) else []
        products = data.get('products', []) if isinstance(data, dict) else data
        if not isinstance(products, list):
            products = []

        for u in users:
            login = (u.get('login', '') or '').strip()
            if login and not self.LoginExists(login):
                self.db.execute(
                    "INSERT INTO users VALUES(NULL,?,?,?,?,?,?,?)",
                    (u.get('name',''), u.get('surname',''),
                     u.get('patronymic',''), login,
                     hash_password('changeme'), u.get('address',''), 0))
                count_u += 1

        for p in products:
            dosage = normalize_dosage(p.get('dosage', ''))
            self.dbc.execute(
                "SELECT id FROM products WHERE name=? AND dosage=?",
                (p.get('name',''), dosage))
            if not self.dbc.fetchone():
                category = normalize_category(p.get('category', DEFAULT_PRODUCT_CATEGORY))
                self.db.execute(
                    "INSERT INTO products(name,dosage,price,in_stock,category) VALUES(?,?,?,?,?)",
                    (
                        p.get('name', ''),
                        dosage,
                        p.get('price', 0),
                        int(p.get('in_stock', True)),
                        category,
                    ),
                )
                count_p += 1

        self.db.commit()
        note = " (пароль по умолчанию: changeme)" if count_u else ""
        return f"Импортировано: {count_u} пользователей{note}, {count_p} товаров"

# ─────────────────────────────────────────────────────────────────
#  Главный класс
# ─────────────────────────────────────────────────────────────────

class Pharmacy:
    def __init__(self):
        self.storage = DBStorage()
        self.io = FlaskInputOutput(request)

    def _is_current_user_admin(self) -> bool:
        return bool(getattr(current_user, 'is_admin', 0))

    def _validate_action_form(self, fallback_endpoint: str):
        form = ActionForm()
        if form.validate_on_submit():
            return True
        flash('Недействительный запрос. Повторите действие.', 'error')
        return redirect(module_url(fallback_endpoint))

    def _get_accessible_order(self, order_id: int):
        order = self.storage.GetOrder(order_id)
        if not order.id:
            flash('Заказ не найден.', 'error')
            return None
        if self._is_current_user_admin():
            return order
        if order.user_id != int(current_user.get_id()):
            flash('У вас нет доступа к этому заказу.', 'error')
            return None
        return order

    # --- Auth ---
    def ShowLogin(self, error=''):
        return render_template('login.tpl', error=error, form=LoginForm())

    def DoLogin(self):
        form = LoginForm()
        if form.validate_on_submit():
            user = self.storage.GetUserByLogin(form.login.data)
            if user:
                is_valid, needs_rehash = verify_password(
                    user.password_hash, form.password.data)
                if is_valid:
                    if needs_rehash:
                        new_hash = hash_password(form.password.data)
                        self.storage.UpdatePassword(user.id, new_hash)
                        user.password_hash = new_hash
                    login_user(user)
                    next_url = request.args.get('next')
                    return redirect(next_url or module_url('my_orders'))
        return self.ShowLogin(error='Неверный логин или пароль')

    def ShowRegister(self, error=''):
        return render_template('register.tpl', error=error, form=RegisterForm())

    def DoRegister(self):
        form = RegisterForm()
        if not form.validate_on_submit():
            error = next(iter(form.errors.values()))[0] if form.errors else ''
            return self.ShowRegister(error=error)

        login = form.login.data.strip()
        if self.storage.LoginExists(login):
            return self.ShowRegister(error='Логин уже занят')

        u = UserItem(
            name       = (form.name.data or '').strip(),
            surname    = (form.surname.data or '').strip(),
            patronymic = (form.patronymic.data or '').strip(),
            login      = login,
            password_hash = hash_password(form.password.data),
            address    = (form.address.data or '').strip(),
        )
        self.storage.RegisterUser(u)
        self.storage.db.commit()
        user = self.storage.GetUserByLogin(login)
        login_user(user)
        return redirect(module_url('my_orders'))

    def DoLogout(self):
        action_result = self._validate_action_form('products')
        if action_result is not True:
            return action_result
        logout_user()
        return redirect(module_url('login'))

    # --- Admin ---
    def ShowAdmin(self):
        return render_template(
            'admin.tpl',
            users=list(self.storage.GetUsers()),
            products=list(self.storage.GetProducts()),
            action_form=ActionForm(),
        )

    def ShowAdminUserForm(self, user_id):
        item = self.storage.GetUser(user_id)
        form = AdminUserForm(obj=item)
        return render_template('admin_user_form.tpl', it=item, form=form, error='')

    def SaveAdminUser(self):
        item = self.storage.GetUser(int(request.form.get('id') or 0))
        form = AdminUserForm()
        if not form.validate_on_submit():
            error = next(iter(form.errors.values()))[0] if form.errors else ''
            return render_template('admin_user_form.tpl', it=item, form=form, error=error)

        login = (form.login.data or '').strip()
        if self.storage.LoginExists(login, item.id):
            return render_template(
                'admin_user_form.tpl', it=item, form=form,
                error='Логин уже занят')

        password = form.password.data or ''
        confirm = form.confirm.data or ''
        if not item.id and not password:
            return render_template(
                'admin_user_form.tpl', it=item, form=form,
                error='Укажите пароль для нового пользователя')
        if password and password != confirm:
            return render_template(
                'admin_user_form.tpl', it=item, form=form,
                error='Пароли не совпадают')

        item.name = (form.name.data or '').strip()
        item.surname = (form.surname.data or '').strip()
        item.patronymic = (form.patronymic.data or '').strip()
        item.login = login
        item.address = (form.address.data or '').strip()
        item.is_admin = int(form.is_admin.data or 0)
        if item.id == int(current_user.get_id()):
            item.is_admin = 1
        if password:
            item.password_hash = hash_password(password)

        if item.id:
            self.storage.UpdateUser(item)
            if password:
                self.storage.UpdatePassword(item.id, item.password_hash)
        else:
            self.storage.RegisterUser(item)
        return redirect(module_url('admin'))

    def DeleteAdminUser(self, user_id):
        action_result = self._validate_action_form('admin')
        if action_result is not True:
            return action_result
        if user_id == int(current_user.get_id()):
            flash('Нельзя удалить текущего администратора.', 'warning')
            return redirect(module_url('admin'))
        user = self.storage.GetUser(user_id)
        if user.id:
            self.storage.DeleteUser(user.id)
            flash('Пользователь удалён.', 'success')
        else:
            flash('Пользователь не найден.', 'error')
        return redirect(module_url('admin'))

    # --- Профиль ---
    def ShowProfile(self):
        user = self.storage.GetUser(int(current_user.get_id()))
        form = ProfileForm(obj=user)
        return render_template('profile.tpl', it=user, form=form)

    def SaveProfile(self):
        user = self.storage.GetUser(int(current_user.get_id()))
        form = ProfileForm()
        if not form.validate_on_submit():
            return render_template('profile.tpl', it=user, form=form)

        user.name = form.name.data or ''
        user.surname = form.surname.data or ''
        user.patronymic = form.patronymic.data or ''
        user.login = form.login.data or ''
        user.address = form.address.data or ''
        self.storage.UpdateUser(user)

        if form.new_password.data:
            is_valid, _ = verify_password(
                user.password_hash, form.current_password.data or '')
            if is_valid and form.new_password.data == form.confirm_password.data:
                self.storage.UpdatePassword(user.id, hash_password(form.new_password.data))
        return redirect(module_url('profile'))

    # --- Каталог (публичный) ---
    def ShowProducts(self):
        search_query = (request.args.get('q') or '').strip()
        selected_category = (request.args.get('category') or 'Все').strip() or 'Все'
        if selected_category != 'Все' and selected_category not in PRODUCT_CATEGORIES:
            selected_category = 'Все'
        return render_template('products.tpl',
                               products=list(
                                   self.storage.GetProducts(
                                       query=search_query,
                                       category=selected_category,
                                   )
                               ),
                               search_query=search_query,
                               selected_category=selected_category,
                               category_options=('Все', *PRODUCT_CATEGORIES),
                               action_form=ActionForm())

    def ShowProductForm(self, id):
        item = self.storage.GetProduct(id)
        form = ProductForm(obj=item)
        return render_template('product_form.tpl', it=item, form=form)

    def AddProduct(self):
        item = self.storage.GetProduct(int(request.form.get('id') or 0))
        form = ProductForm()
        if form.validate_on_submit():
            item.name = form.name.data
            item.dosage = normalize_dosage(form.dosage.data or '')
            item.category = normalize_category(form.category.data or DEFAULT_PRODUCT_CATEGORY)
            item.price = form.price.data
            item.in_stock = form.in_stock.data
            self.storage.AddProduct(item)
            return redirect(module_url('admin'))
        return render_template('product_form.tpl', it=item, form=form)

    def DeleteProduct(self, id):
        action_result = self._validate_action_form('admin')
        if action_result is not True:
            return action_result
        self.storage.DeleteProduct(id)
        flash('Товар удалён.', 'success')
        return redirect(module_url('admin'))

    # --- Корзина в session ---
    def GetCartItems(self):
        cart = get_cart()
        clean_cart = {}
        items = []
        removed_count = 0
        for raw_product_id, raw_quantity in cart.items():
            try:
                product_id = int(raw_product_id)
                quantity = normalize_cart_quantity(raw_quantity)
            except (TypeError, ValueError):
                removed_count += 1
                continue

            if quantity <= 0:
                removed_count += 1
                continue

            product = self.storage.GetProduct(product_id)
            if not product.id or not product.in_stock:
                removed_count += 1
                continue

            clean_cart[str(product.id)] = quantity
            items.append({
                'product': product,
                'quantity': quantity,
                'line_total': product.price * quantity,
            })

        if clean_cart != cart:
            save_cart(clean_cart)
            if removed_count:
                flash('Некоторые товары больше недоступны и были удалены из корзины.', 'warning')
        return items

    def ShowCart(self):
        items = self.GetCartItems()
        total = sum(item['line_total'] for item in items)
        return render_template(
            'cart.tpl',
            items=items,
            total=total,
            action_form=ActionForm(),
        )

    def AddToCart(self, product_id):
        action_result = self._validate_action_form('products')
        if action_result is not True:
            return action_result
        product = self.storage.GetProduct(product_id)
        if product.id and product.in_stock:
            cart = get_cart()
            key = str(product.id)
            current_quantity = normalize_cart_quantity(cart.get(key, 0))
            if current_quantity >= CART_MAX_QUANTITY:
                cart[key] = CART_MAX_QUANTITY
                save_cart(cart)
                flash('Достигнуто максимальное количество этого товара в корзине.', 'warning')
                return redirect(module_url('cart'))
            cart[key] = current_quantity + 1
            save_cart(cart)
            flash('Товар добавлен в корзину.', 'success')
            return redirect(module_url('cart'))
        flash('Товар не найден или недоступен для заказа.', 'error')
        return redirect(module_url('products'))

    def RemoveFromCart(self, product_id):
        action_result = self._validate_action_form('cart')
        if action_result is not True:
            return action_result
        cart = get_cart()
        if str(product_id) in cart:
            cart.pop(str(product_id), None)
            flash('Товар удалён из корзины.', 'success')
        else:
            flash('Этого товара уже нет в корзине.', 'warning')
        save_cart(cart)
        return redirect(module_url('cart'))

    def CheckoutCart(self):
        action_result = self._validate_action_form('cart')
        if action_result is not True:
            return action_result
        items = self.GetCartItems()
        if not items:
            flash('Корзина пуста. Добавьте товары перед оформлением заказа.', 'warning')
            return redirect(module_url('cart'))

        order = OrderItem(
            user_id=int(current_user.get_id()),
            payment=PAYMENT_CASH,
        )
        for item in items:
            product = item['product']
            for _ in range(item['quantity']):
                order.items.append({
                    'name': product.name,
                    'dosage': normalize_dosage(product.dosage),
                    'price': product.price,
                })

        self.storage.AddOrder(order)
        session.pop('cart', None)
        session.modified = True
        flash('Заказ создан.', 'success')
        return redirect(module_url('my_orders'))

    # --- Заказы (только своего пользователя) ---
    def ShowMyOrders(self):
        user = self.storage.GetUser(int(current_user.get_id()))
        orders = list(self.storage.GetUserOrders(user.id))
        return render_template(
            'orders.tpl',
            user=user,
            orders=orders,
            action_form=ActionForm(),
        )

    def ShowOrderForm(self, order_id):
        user_id = int(current_user.get_id())
        if order_id > 0:
            order = self._get_accessible_order(order_id)
            if order is None:
                return redirect(module_url('my_orders'))
        else:
            order = OrderItem(user_id=user_id, payment=PAYMENT_CASH)
        if not self._is_current_user_admin():
            order.user_id = user_id
        products = list(self.storage.GetProducts())
        form = OrderForm(obj=order)
        form.product_ids.choices = [(p.id, f'{p.name} {p.dosage}') for p in products]
        form.payment.data = PAYMENT_CASH
        form.product_ids.data = [
            p.id for p in products
            if any(i['name'] == p.name and i['dosage'] == p.dosage for i in order.items)
        ]
        if form.product_ids.data is None:
            form.product_ids.data = []
        return render_template('order_form.tpl', it=order, products=products, form=form)

    def AddOrder(self):
        user_id = int(current_user.get_id())
        order_id = int(request.form.get('id') or 0)
        if order_id > 0:
            item = self._get_accessible_order(order_id)
            if item is None:
                return redirect(module_url('my_orders'))
        else:
            item = OrderItem()
        if self._is_current_user_admin():
            if not item.id:
                item.user_id = user_id
        else:
            item.user_id = user_id
        products = list(self.storage.GetProducts())
        form = OrderForm()
        form.product_ids.choices = [(p.id, f'{p.name} {p.dosage}') for p in products]
        form.payment.data = PAYMENT_CASH
        if form.product_ids.data is None:
            form.product_ids.data = []
        if form.validate_on_submit():
            item.payment = PAYMENT_CASH
            item.items = []
            for pid in form.product_ids.data:
                p = self.storage.GetProduct(pid)
                if p.id and p.in_stock:
                    item.items.append({
                        'name': p.name, 'dosage': normalize_dosage(p.dosage), 'price': p.price
                    })
            self.storage.AddOrder(item)
            return redirect(module_url('my_orders'))
        return render_template('order_form.tpl', it=item, products=products, form=form)

    def DeleteOrder(self, order_id):
        action_result = self._validate_action_form('my_orders')
        if action_result is not True:
            return action_result
        order = self._get_accessible_order(order_id)
        if order is None:
            return redirect(module_url('my_orders'))
        self.storage.DeleteOrder(order.id)
        flash('Заказ удалён.', 'success')
        return redirect(module_url('my_orders'))

    # --- Импорт ---
    def ImportPickle(self):
        action_result = self._validate_action_form('admin')
        if action_result is not True:
            return action_result
        path = get_import_path()
        msg = self.storage.ImportFromPickle(path)
        return render_template('import.tpl', msg=msg, path=path)


# ─────────────────────────────────────────────────────────────────
#  Per-request singleton
# ─────────────────────────────────────────────────────────────────

def get_pharmacy():
    if 'pharmacy' not in g:
        g.pharmacy = Pharmacy()
    return g.pharmacy


@bp.teardown_app_request
def teardown(ctx):
    p = g.pop('pharmacy', None)
    if p is not None:
        try:
            p.storage.Store()
        except Exception:
            pass


# ─────────────────────────────────────────────────────────────────
#  Маршруты
# ─────────────────────────────────────────────────────────────────

# Auth
@bp.route("/login", methods=['GET'])
def login():
    if current_user.is_authenticated:
        return redirect(module_url('my_orders'))
    return get_pharmacy().ShowLogin()

@bp.route("/login", methods=['POST'])
def login_post():
    return get_pharmacy().DoLogin()

@bp.route("/register", methods=['GET'])
def register():
    return get_pharmacy().ShowRegister()

@bp.route("/register", methods=['POST'])
def register_post():
    return get_pharmacy().DoRegister()

@bp.route("/logout", methods=['POST'])
def logout():
    return get_pharmacy().DoLogout()

# Admin
@bp.route("/admin")
@admin_required
def admin():
    return get_pharmacy().ShowAdmin()

@bp.route("/admin/users/form/<int:user_id>")
@admin_required
def admin_user_form(user_id):
    return get_pharmacy().ShowAdminUserForm(user_id)

@bp.route("/admin/users/save", methods=['POST'])
@admin_required
def admin_user_save():
    return get_pharmacy().SaveAdminUser()

@bp.route("/admin/users/delete/<int:user_id>", methods=['POST'])
@admin_required
def admin_user_delete(user_id):
    return get_pharmacy().DeleteAdminUser(user_id)

# Профиль
@bp.route("/profile", methods=['GET'])
@login_required
def profile():
    return get_pharmacy().ShowProfile()

@bp.route("/profile", methods=['POST'])
@login_required
def profile_save():
    return get_pharmacy().SaveProfile()

# Каталог (доступен всем)
@bp.route("/")
@bp.route("/products")
def products():
    return get_pharmacy().ShowProducts()

@bp.route("/products/form/<int:id>")
@admin_required
def product_form(id):
    return get_pharmacy().ShowProductForm(id)

@bp.route("/products/add", methods=['POST'])
@admin_required
def product_add():
    return get_pharmacy().AddProduct()

@bp.route("/products/delete/<int:id>", methods=['POST'])
@admin_required
def product_delete(id):
    return get_pharmacy().DeleteProduct(id)

# Корзина
@bp.route("/cart")
@login_required
def cart():
    return get_pharmacy().ShowCart()

@bp.route("/cart/add/<int:product_id>", methods=['POST'])
@login_required
def cart_add(product_id):
    return get_pharmacy().AddToCart(product_id)

@bp.route("/cart/remove/<int:product_id>", methods=['POST'])
@login_required
def cart_remove(product_id):
    return get_pharmacy().RemoveFromCart(product_id)

@bp.route("/cart/checkout", methods=['POST'])
@login_required
def cart_checkout():
    return get_pharmacy().CheckoutCart()

# Мои заказы
@bp.route("/orders")
@login_required
def my_orders():
    return get_pharmacy().ShowMyOrders()

@bp.route("/orders/form/<int:order_id>")
@login_required
def order_form(order_id):
    return get_pharmacy().ShowOrderForm(order_id)

@bp.route("/orders/add", methods=['POST'])
@login_required
def order_add():
    return get_pharmacy().AddOrder()

@bp.route("/orders/delete/<int:order_id>", methods=['POST'])
@login_required
def order_delete(order_id):
    return get_pharmacy().DeleteOrder(order_id)

# Импорт
@bp.route("/import", methods=['POST'])
@admin_required
def import_pickle():
    return get_pharmacy().ImportPickle()
