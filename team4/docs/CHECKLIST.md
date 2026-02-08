# ✅ Team 4 Backend Deployment Checklist

## Phase 1: Environment Setup (5 minutes)

```powershell
# 1. Install required packages
pip install djangorestframework django-filter requests Pillow mysqlclient

# 2. Verify installation
pip list | Select-String "django"
```

**Checkpoints:**
- [ ] djangorestframework installed
- [ ] django-filter installed  
- [ ] requests installed
- [ ] Pillow installed
- [ ] mysqlclient installed

---

## Phase 2: Database Configuration & Migrations (5 minutes)

```powershell
cd e:\alirreza\cds\uni\SE\project\BugOff\Software-Engineering-1404-01_G2

# 1. Create MySQL database (in MySQL Workbench or CLI)
# CREATE DATABASE IF NOT EXISTS team4_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 2. Verify .env file contains:
# TEAM4_DATABASE_URL=mysql://root:YOUR_PASSWORD@localhost:3306/team4_db

# 3. Generate migrations
python manage.py makemigrations team4

# 4. Apply migrations to team4 database
python manage.py migrate --database=team4
```

**Checkpoints:**
- [ ] Database `team4_db` created in MySQL
- [ ] `.env` file configured correctly
- [ ] `makemigrations` executed without errors
- [ ] `migrate --database=team4` executed successfully
- [ ] "Applied X migrations" message displayed

---

## Phase 3: Data Loading (3 minutes)

```powershell
# Load provinces (31 records)
python manage.py load_provinces

# Load cities (1112 records)  
python manage.py load_cities

# Verify data
python manage.py show_stats
```

**Checkpoints:**
- [ ] 31 provinces loaded successfully
- [ ] 1112 cities loaded with geolocation data
- [ ] Statistics command shows correct counts
- [ ] No database errors during loading

---

## Phase 4: Create Superuser (1 minute)

```powershell
python manage.py createsuperuser
```

**Credentials:**
- Username: `admin`
- Email: `admin@example.com`
- Password: `admin123`

**Checkpoint:**
- [ ] Superuser created successfully

---

## Phase 5: Start Development Server (1 minute)

```powershell
python manage.py runserver
```

**Checkpoints:**
- [ ] Server started without errors
- [ ] "Starting development server at http://127.0.0.1:8000/" message displayed
- [ ] No port conflicts

---

## Phase 6: API Testing (10 minutes)

### Browser Testing:

#### 1. Django Admin
- [ ] Accessible at: http://localhost:8000/admin/
- [ ] Login with admin/admin123 successful
- [ ] Team4 models visible in admin panel

#### 2. API Root
- [ ] Accessible at: http://localhost:8000/team4/api/
- [ ] Endpoint list displayed correctly

#### 3. Geography Endpoints
- [ ] Provinces: http://localhost:8000/team4/api/provinces/
  - Returns 31 provinces with geolocation
- [ ] Cities: http://localhost:8000/team4/api/cities/
  - Returns 1112 cities with coordinates
- [ ] Cities by province: http://localhost:8000/team4/api/cities/?province=Tehran
  - Filters correctly by province

#### 4. Categories Endpoint
- [ ] Accessible at: http://localhost:8000/team4/api/categories/
- [ ] Returns category list

#### 5. Amenities Endpoint
- [ ] Accessible at: http://localhost:8000/team4/api/amenities/
- [ ] Returns amenity list

#### 6. Facilities Endpoint (when data added)
- [ ] List: http://localhost:8000/team4/api/facilities/
- [ ] Filter by city: `?city=Tehran`
- [ ] Filter by category: `?category=Hotel`
- [ ] Filter by rating: `?min_rating=4`
- [ ] Details: http://localhost:8000/team4/api/facilities/1/
- [ ] Nearby: http://localhost:8000/team4/api/facilities/1/nearby/?radius=5

### PowerShell/cURL Testing:

```powershell
# Test provinces
curl http://localhost:8000/team4/api/provinces/

# Test cities
curl http://localhost:8000/team4/api/cities/

# Test facilities (after adding data)
curl http://localhost:8000/team4/api/facilities/

# Test facility details
curl http://localhost:8000/team4/api/facilities/1/

# Test nearby facilities
curl http://localhost:8000/team4/api/facilities/1/nearby/?radius=5

# Test comparison
curl -X POST http://localhost:8000/team4/api/facilities/compare/ `
  -H "Content-Type: application/json" `
  -d '{\"facility_ids\": [1, 2]}'
```

**Checkpoints:**
- [ ] All GET endpoints return 200 OK
- [ ] JSON responses are valid
- [ ] Geolocation data (latitude/longitude) present in responses
- [ ] Filtering parameters work correctly

---

## Phase 7: Unit Testing (3 minutes)

```powershell
# Run all tests
python manage.py test team4

# Run specific test modules
python manage.py test team4.tests.test_models
python manage.py test team4.tests.test_services

# Run with verbose output
python manage.py test team4 --verbosity=2
```

**Checkpoints:**
- [ ] All tests pass
- [ ] No test failures or errors
- [ ] "OK" message displayed
- [ ] Coverage report generated (if configured)

---

## Phase 8: Add Sample Data via Admin (15 minutes)

Navigate to http://localhost:8000/admin/team4/facility/

Add the following facilities:

### Hotels (5):
- [ ] Hotel 1: Tehran, 4+ stars
- [ ] Hotel 2: Shiraz, 4+ stars  
- [ ] Hotel 3: Isfahan, 3+ stars
- [ ] Hotel 4: Mashhad, 4+ stars
- [ ] Hotel 5: Tabriz, 3+ stars

### Restaurants (3):
- [ ] Restaurant 1: Tehran, Persian cuisine
- [ ] Restaurant 2: Shiraz, Traditional
- [ ] Restaurant 3: Isfahan, Fast food

### Hospitals (2):
- [ ] Hospital 1: Tehran
- [ ] Hospital 2: Shiraz

For each facility, ensure:
- [ ] Persian and English names provided
- [ ] Category selected
- [ ] City selected (from 1112 cities)
- [ ] Address filled
- [ ] Valid coordinates (latitude/longitude from map)
- [ ] At least 1 pricing entry
- [ ] At least 1 image
- [ ] 2-3 amenities selected

---

## Phase 9: Integration Testing (5 minutes)

```powershell
# Test search functionality
curl "http://localhost:8000/team4/api/facilities/?city=Tehran"

# Test filtering
curl "http://localhost:8000/team4/api/facilities/?city=Tehran&min_rating=4"

# Test details
curl http://localhost:8000/team4/api/facilities/1/

# Test nearby with different radius
curl http://localhost:8000/team4/api/facilities/1/nearby/?radius=10

# Test comparison
curl -X POST http://localhost:8000/team4/api/facilities/compare/ `
  -H "Content-Type: application/json" `
  -d '{\"facility_ids\": [1, 2, 3]}'
```

**Checkpoints:**
- [ ] Search returns correct results
- [ ] Filters work as expected
- [ ] Geolocation calculations accurate
- [ ] Distance calculations reasonable
- [ ] Comparison shows differences clearly

---

## Phase 10: Version Control (5 minutes)

```powershell
# Create feature branch
git checkout -b team4-geolocation-features

# Stage files
git add team4/
git add requirements.txt

# Commit changes
git commit -m "feat(team4): Add geolocation-based facility management

- Implement MySQL POINT field without GeoDjango
- Add 31 provinces with coordinates
- Add 1112 cities with geolocation data
- Create facility management APIs
- Add distance calculation and nearby search
- Implement facility comparison feature"

# Push to remote
git push origin team4-geolocation-features
```

**Checkpoints:**
- [ ] Branch created successfully
- [ ] All changes committed
- [ ] Push completed without conflicts
- [ ] Pull request can be created

---

## ✅ Deployment Completion Checklist

Verify all the following before marking complete:

### Infrastructure
- [ ] MySQL database configured and accessible
- [ ] All migrations applied successfully
- [ ] 31 provinces loaded with geolocation
- [ ] 1112 cities loaded with coordinates

### API Endpoints
- [ ] Provinces API functional
- [ ] Cities API functional with province filtering
- [ ] Categories API functional
- [ ] Amenities API functional
- [ ] Facilities API functional
- [ ] Search and filter working
- [ ] Nearby facilities search working
- [ ] Facility comparison working

### Data Integrity
- [ ] At least 10 sample facilities added
- [ ] Geolocation data valid for all entries
- [ ] All foreign keys properly linked
- [ ] No orphaned records

### Testing
- [ ] All unit tests passing
- [ ] Integration tests successful
- [ ] API responses validated
- [ ] Performance acceptable

### Documentation
- [ ] Code comments present
- [ ] API endpoints documented
- [ ] README updated
- [ ] This checklist completed

---

## 🎉 Success Criteria

Your backend deployment is complete when:

✅ **Database**: 31 provinces + 1112 cities with geolocation  
✅ **APIs**: 8+ functional endpoints  
✅ **Features**: Search, filter, nearby, comparison  
✅ **Data**: 10+ sample facilities with complete info  
✅ **Tests**: All passing with >70% coverage  
✅ **Docs**: Complete and up-to-date  

**Backend is production-ready! 🚀**

---

## 🐛 Common Issues & Solutions

### Error: `No module named 'rest_framework'`
```powershell
pip install djangorestframework
```

### Error: `Table doesn't exist`
```powershell
python manage.py migrate --database=team4
```

### Error: `Invalid POINT value`
```powershell
# Check that coordinates are in format: POINT(longitude latitude)
# Ensure ST_GeomFromText is used in SQL
```

### Error: `Port already in use`
```powershell
python manage.py runserver 8001
```

### Error: `Connection refused`
```powershell
# Check MySQL service is running
# Verify .env database credentials
```

---

## 📚 Additional Resources

- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [MySQL Spatial Data Types](https://dev.mysql.com/doc/refman/8.0/en/spatial-types.html)
- [Project README](../README.md)
- [Setup Guide](SETUP_GUIDE.md)
- [Project Summary](SUMMARY.md)

**Questions?** Contact the development team.

---

**Last Updated**: February 8, 2026  
**Version**: 1.0.0  
**Status**: Production Ready ✅

---

## مرحله 4: ایجاد Superuser (1 دقیقه)

```powershell
python manage.py createsuperuser
```

وارد کنید:
- Username: `admin`
- Email: `admin@example.com`
- Password: `admin123`

- [ ] Superuser ساخته شد

---

## مرحله 5: اجرای سرور (1 دقیقه)

```powershell
python manage.py runserver
```

- [ ] سرور بدون خطا اجرا شد
- [ ] پیام "Starting development server at http://127.0.0.1:8000/" نمایش داده شد

---

## مرحله 6: تست APIs (5 دقیقه)

### با مرورگر:

1. Django Admin:
   - [ ] باز شد: http://localhost:8000/admin/
   - [ ] وارد شدید با admin/admin123
   - [ ] Team4 > Facilities > دیده می‌شه

2. API Root:
   - [ ] باز شد: http://localhost:8000/team4/api/
   - [ ] لیست endpoints نمایش داده شد

3. Categories:
   - [ ] باز شد: http://localhost:8000/team4/api/categories/
   - [ ] 8 دسته‌بندی نمایش داده شد

4. Cities:
   - [ ] باز شد: http://localhost:8000/team4/api/cities/
   - [ ] 5 شهر نمایش داده شد

5. Facilities:
   - [ ] باز شد: http://localhost:8000/team4/api/facilities/
   - [ ] 5 مکان نمایش داده شد

6. جستجو:
   - [ ] باز شد: http://localhost:8000/team4/api/facilities/?city=شیراز
   - [ ] نتایج فقط شیراز نمایش داده شد

7. فیلتر:
   - [ ] باز شد: http://localhost:8000/team4/api/facilities/?min_rating=4
   - [ ] فقط مکان‌های با امتیاز 4+ نمایش داده شد

8. جزئیات:
   - [ ] باز شد: http://localhost:8000/team4/api/facilities/1/
   - [ ] جزئیات کامل با amenities و pricing نمایش داده شد

9. Nearby:
   - [ ] باز شد: http://localhost:8000/team4/api/facilities/1/nearby/
   - [ ] امکانات نزدیک با فاصله نمایش داده شد

---

## مرحله 7: اجرای Tests (2 دقیقه)

```powershell
# تست همه
python manage.py test team4

# تست Models
python manage.py test team4.tests.test_models

# تست Services
python manage.py test team4.tests.test_services
```

- [ ] تست‌ها بدون خطا اجرا شدند
- [ ] همه تست‌ها PASS شدند
- [ ] پیام "OK" نمایش داده شد

---

## مرحله 8: افزودن داده (10 دقیقه)

از Django Admin:

1. برو به http://localhost:8000/admin/team4/facility/
2. کلیک "Add Facility"
3. اضافه کن:

   - [ ] 5 هتل دیگه در شیراز
   - [ ] 3 رستوران دیگه در شیراز
   - [ ] 2 بیمارستان دیگه در شیراز
   - [ ] 2 مکان در تهران
   - [ ] 2 مکان در اصفهان

برای هر مکان:
- [ ] نام فارسی و انگلیسی
- [ ] دسته‌بندی
- [ ] شهر
- [ ] آدرس
- [ ] Latitude/Longitude
- [ ] حداقل 1 قیمت
- [ ] حداقل 1 تصویر
- [ ] 2-3 امکانات

---

## مرحله 9: تست نهایی (5 دقیقه)

```powershell
# تست جستجو
curl http://localhost:8000/team4/api/facilities/?city=شیراز

# تست فیلتر
curl "http://localhost:8000/team4/api/facilities/?city=شیراز&min_rating=4"

# تست جزئیات
curl http://localhost:8000/team4/api/facilities/1/

# تست nearby
curl http://localhost:8000/team4/api/facilities/1/nearby/?radius=5
```

- [ ] همه APIها بدون خطا کار می‌کنند
- [ ] داده‌ها صحیح برگشته می‌شوند
- [ ] JSON valid هست

---

## مرحله 10: Git (5 دقیقه)

```powershell
# ساخت branch
git checkout -b team4-feature-facilities

# اضافه کردن فایل‌ها
git add team4/
git add requirements.txt
git add app404/settings.py

# Commit
git commit -m "Add Models, Services, APIs for Facilities - Team4"

# Push
git push origin team4-feature-facilities
```

- [ ] Branch ساخته شد
- [ ] فایل‌ها commit شدند
- [ ] Push بدون خطا انجام شد

---

## ✅ نتیجه نهایی

اگه همه موارد بالا چک شده باشن:

🎉 **تبریک! شما قسمت Backend Core رو کامل کردید!**

حالا می‌تونید:
1. به تیم اطلاع بدید که Backend آماده‌ست
2. به نفر 3 کمک کنید برای یکپارچگی APIs
3. داده‌های بیشتر اضافه کنید
4. منتظر Frontend نفر 4 باشید

---

## 🐛 مشکلات رایج

### خطا: No module named 'rest_framework'
```powershell
pip install djangorestframework
```

### خطا: No such table
```powershell
python manage.py migrate
```

### خطا: Fixture not found
```powershell
# مطمئن شو در پوشه اصلی هستی
cd e:\alirreza\cds\uni\SE\project\BugOff\Software-Engineering-1404-01_G2
python manage.py loaddata team4/fixtures/provinces.json
```

### خطا: Port in use
```powershell
python manage.py runserver 8001
```

---

## 📞 کمک بیشتر

- 📖 README.md - مستندات کلی
- 🚀 SETUP_GUIDE.md - راهنمای گام‌به‌گام
- 📋 SUMMARY.md - خلاصه کامل
- ✅ این فایل! - Checklist

**موفق باشید! 🎯**
