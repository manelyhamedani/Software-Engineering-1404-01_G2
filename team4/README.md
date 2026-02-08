# Team 4 - Facilities & Transportation Service

سرویس مدیریت امکانات (هتل، رستوران، بیمارستان) و خدمات حمل‌ونقل

## 📋 مراحل راه‌اندازی

### 1. نصب Dependencies

```bash
pip install -r requirements.txt
pip install mysqlclient  # برای MySQL
```

### 2. تنظیمات Database

**الف) ساخت Database در MySQL:**

```sql
CREATE DATABASE IF NOT EXISTS team4_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**ب) تنظیم فایل `.env`:**

در فایل `.env` در root پروژه این خط را اضافه کنید:

```env
TEAM4_DATABASE_URL=mysql://root:YOUR_MYSQL_PASSWORD@localhost:3306/team4_db
```

### 3. تنظیمات Django

مطمئن شوید `team4` در `INSTALLED_APPS` اضافه شده:

```python
# app404/settings.py
INSTALLED_APPS = [
    ...
    'rest_framework',
    'django_filters',
    'team4',
]
```

### 4. Migrations

```bash
python manage.py makemigrations team4
python manage.py migrate --database=team4
```

### 5. بارگذاری داده‌های اولیه

```bash
python manage.py loaddata team4/fixtures/provinces.json --database=team4
python -m team4.load_cities  # Cities با Python script
python manage.py loaddata team4/fixtures/categories.json --database=team4
python manage.py loaddata team4/fixtures/amenities.json --database=team4
```

### 5. ایجاد Superuser

```bash
python manage.py createsuperuser
```

### 6. اجرای سرور

```bash
python manage.py runserver
```

---

## 🔌 API Endpoints

### امکانات (Facilities)

#### 1. لیست امکانات با جستجو و فیلتر
```http
GET /team4/api/facilities/

Query Parameters:
- city: نام شهر (مثال: شیراز)
- category: نام دسته‌بندی (مثال: هتل)
- min_price: حداقل قیمت
- max_price: حداکثر قیمت
- min_rating: حداقل امتیاز (1-5)
- amenities: لیست amenity_id (کاما-separated، مثال: 1,2,5)
- is_24_hour: فیلتر 24 ساعته (true/false)
- sort: نوع مرتب‌سازی (distance|rating|review_count)
- page: شماره صفحه
- page_size: تعداد در هر صفحه (پیش‌فرض: 10)
```

**مثال:**
```bash
curl "http://localhost:8000/team4/api/facilities/?city=شیراز&category=هتل&min_rating=4&sort=rating"
```

#### 2. جزئیات یک مکان
```http
GET /team4/api/facilities/{fac_id}/
```

**مثال:**
```bash
curl "http://localhost:8000/team4/api/facilities/1/"
```

#### 3. امکانات نزدیک
```http
GET /team4/api/facilities/{fac_id}/nearby/

Query Parameters:
- radius: شعاع جستجو (km، پیش‌فرض: 5)
- category: فیلتر دسته‌بندی (اختیاری)
```

**مثال:**
```bash
curl "http://localhost:8000/team4/api/facilities/1/nearby/?radius=5&category=رستوران"
```

#### 4. مقایسه هتل‌ها
```http
POST /team4/api/facilities/compare/

Body (JSON):
{
  "facility_ids": [1, 2, 3]
}
```

**مثال:**
```bash
curl -X POST "http://localhost:8000/team4/api/facilities/compare/" \
  -H "Content-Type: application/json" \
  -d '{"facility_ids": [1, 2]}'
```

---

### دسته‌بندی‌ها (Categories)

```http
GET /team4/api/categories/
GET /team4/api/categories/{id}/
```

---

### شهرها (Cities)

```http
GET /team4/api/cities/
GET /team4/api/cities/{id}/

Query Parameters:
- province: فیلتر بر اساس نام استان
```

**مثال:**
```bash
curl "http://localhost:8000/team4/api/cities/?province=فارس"
```

---

### امکانات (Amenities)

```http
GET /team4/api/amenities/
GET /team4/api/amenities/{id}/
```

---

## 🧪 اجرای تست‌ها

### تست همه Models و Services
```bash
python manage.py test team4
```

### تست فقط Models
```bash
python manage.py test team4.tests.test_models
```

### تست فقط Services
```bash
python manage.py test team4.tests.test_services
```

### تست با Coverage
```bash
pip install coverage
coverage run --source='team4' manage.py test team4
coverage report
coverage html
```

---

## 📊 مدیریت از Django Admin

دسترسی به پنل ادمین:
```
http://localhost:8000/admin/
```

می‌توانید موارد زیر را مدیریت کنید:
- استان‌ها و شهرها
- دسته‌بندی‌ها
- امکانات (Amenities)
- مکان‌ها (Facilities)
- قیمت‌ها
- تصاویر

---

## 📁 ساختار فایل‌ها

```
team4/
├── models.py              # 8 Model
├── serializers.py         # 8 Serializer
├── views.py               # 4 ViewSet
├── urls.py                # URL Routing
├── admin.py               # Django Admin
├── services/
│   ├── __init__.py
│   └── facility_service.py
├── fixtures/              # داده‌های اولیه
│   ├── provinces.json
│   ├── cities.json
│   ├── categories.json
│   ├── amenities.json
│   └── sample_facilities.json
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   └── test_services.py
└── README.md
```

---

## ✅ Checklist تکمیل شده

- ✅ Models (8 جدول)
- ✅ Migrations
- ✅ Services (Business Logic)
- ✅ Serializers (8 Serializer)
- ✅ ViewSets (4 ViewSet با 9 API)
- ✅ URLs
- ✅ Django Admin
- ✅ Fixtures (داده‌های اولیه)
- ✅ Tests (Models + Services)
- ✅ Documentation

---

## 🚀 مراحل بعدی

1. **تست APIs با Postman/Thunder Client**
2. **اضافه کردن داده‌های بیشتر از طریق Admin**
3. **پیاده‌سازی Frontend توسط نفر 4**
4. **یکپارچگی با Neshan API (نفر 2)**
5. **یکپارچگی با سایر سرویس‌ها (Map, Trip Plan)**

---

## 📞 تماس

**تیم 4 - Facilities & Transportation**
- Backend Core: شما (نفر 1) ✅
- Services & Integration: نفر 2
- APIs & ViewSets: نفر 3
- Frontend: نفر 4
