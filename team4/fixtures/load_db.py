import os
import sys
import django
import json
from pathlib import Path

# Add the project directory to the path
project_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_dir))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app404.settings')
django.setup()

from team4.models import Province, City
from team4.fields import Point


def load_provinces():
    """بارگذاری استان‌ها از فایل JSON"""
    json_path = Path(__file__).parent / 'province.json'
    
    with open(json_path, 'r', encoding='utf-8') as f:
        provinces_data = json.load(f)
    
    print(f"در حال بارگذاری {len(provinces_data)} استان...")
    
    created_count = 0
    updated_count = 0
    
    for prov_data in provinces_data:
        province, created = Province.objects.using('team4').update_or_create(
            province_id=prov_data['id'],
            defaults={
                'name_fa': prov_data['title'],
                'name_en': prov_data['slug'],
            }
        )
        
        if created:
            created_count += 1
            print(f"✓ ایجاد: {province.name_fa}")
        else:
            updated_count += 1
            print(f"○ بروزرسانی: {province.name_fa}")
    
    print(f"\n✅ استان‌ها: {created_count} ایجاد، {updated_count} بروزرسانی")
    return created_count + updated_count


def load_cities():
    """بارگذاری شهرها از فایل JSON"""
    from django.db import connections
    
    json_path = Path(__file__).parent / 'cities.json'
    
    with open(json_path, 'r', encoding='utf-8') as f:
        cities_data = json.load(f)
    
    print(f"\nدر حال بارگذاری {len(cities_data)} شهر...")
    
    created_count = 0
    updated_count = 0
    skipped_count = 0
    
    for city_data in cities_data:
        try:
            # پیدا کردن استان
            province = Province.objects.using('team4').get(province_id=city_data['province_id'])
            
            # چک کردن آیا شهر از قبل وجود دارد
            existing_city = City.objects.using('team4').filter(city_id=city_data['id']).first()
            
            # استفاده از raw SQL برای insert/update با POINT
            with connections['team4'].cursor() as cursor:
                lon = city_data['longitude']
                lat = city_data['latitude']
                
                if existing_city:
                    # Update
                    sql = """
                        UPDATE facilities_city 
                        SET province_id = %s, 
                            name_fa = %s, 
                            name_en = %s, 
                            location = ST_GeomFromText(%s, 4326),
                            updated_at = NOW()
                        WHERE city_id = %s
                    """
                    cursor.execute(sql, [
                        province.province_id,
                        city_data['title'],
                        city_data['slug'],
                        f'POINT({lon} {lat})',
                        city_data['id']
                    ])
                    updated_count += 1
                    if updated_count % 100 == 0:
                        print(f"  {updated_count} شهر بروزرسانی شد...")
                else:
                    # Insert
                    sql = """
                        INSERT INTO facilities_city 
                        (city_id, province_id, name_fa, name_en, location, created_at, updated_at)
                        VALUES (%s, %s, %s, %s, ST_GeomFromText(%s, 4326), NOW(), NOW())
                    """
                    cursor.execute(sql, [
                        city_data['id'],
                        province.province_id,
                        city_data['title'],
                        city_data['slug'],
                        f'POINT({lon} {lat})'
                    ])
                    created_count += 1
                    if created_count % 100 == 0:
                        print(f"  {created_count} شهر ایجاد شد...")
                    
        except Province.DoesNotExist:
            print(f"✗ استان با ID {city_data['province_id']} برای شهر {city_data['title']} یافت نشد")
            skipped_count += 1
        except Exception as e:
            print(f"✗ خطا در پردازش {city_data['title']}: {e}")
            skipped_count += 1
    
    print(f"\n✅ شهرها: {created_count} ایجاد، {updated_count} بروزرسانی، {skipped_count} رد شد")
    return created_count + updated_count


def main():
    """اجرای اسکریپت بارگذاری"""
    print("=" * 60)
    print("بارگذاری داده‌های استان‌ها و شهرها")
    print("=" * 60)
    
    try:
        # ابتدا استان‌ها
        provinces_count = load_provinces()
        
        # سپس شهرها
        cities_count = load_cities()
        
        print("\n" + "=" * 60)
        print(f"✅ بارگذاری کامل شد!")
        print(f"   استان‌ها: {provinces_count}")
        print(f"   شهرها: {cities_count}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ خطا: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
