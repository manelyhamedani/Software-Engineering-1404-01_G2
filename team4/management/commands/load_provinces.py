from django.core.management.base import BaseCommand
from team4.models import Province
from team4.fields import Point
import json


class Command(BaseCommand):
    help = 'Load provinces with location data'

    def handle(self, *args, **options):
        fixture_path = 'team4/fixtures/province.json'
        
        with open(fixture_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        updated_count = 0
        created_count = 0
        
        for item in data:
            pk = item['pk']
            fields = item['fields']
            
            # پردازش location
            location = None
            if fields.get('location'):
                location_str = fields['location']
                # پارس کردن "POINT(lng lat)"
                coords = location_str.replace('POINT(', '').replace(')', '').split()
                lng = float(coords[0])
                lat = float(coords[1])
                location = Point(lng, lat)
            
            # بررسی اینکه آیا استان وجود دارد
            try:
                province = Province.objects.using('team4').get(province_id=pk)
                # Update existing province
                province.name_fa = fields['name_fa']
                province.name_en = fields['name_en']
                province.location = location
                province.save(using='team4', update_fields=['name_fa', 'name_en', 'location', 'updated_at'])
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ بروزرسانی: {province.name_fa}'))
            except Province.DoesNotExist:
                # Create new province
                province = Province(
                    province_id=pk,
                    name_fa=fields['name_fa'],
                    name_en=fields['name_en'],
                    location=location
                )
                province.save(using='team4')
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ ایجاد: {province.name_fa}'))
        
        self.stdout.write(self.style.SUCCESS(
            f'\n✅ کامل شد: {created_count} ایجاد، {updated_count} بروزرسانی'
        ))
