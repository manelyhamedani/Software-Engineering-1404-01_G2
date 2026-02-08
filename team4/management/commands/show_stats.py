from django.core.management.base import BaseCommand
from team4.models import City, Province


class Command(BaseCommand):
    help = 'Show database statistics'

    def handle(self, *args, **options):
        province_count = Province.objects.using('team4').count()
        city_count = City.objects.using('team4').count()
        
        self.stdout.write(self.style.SUCCESS(f'\n📊 آمار دیتابیس:'))
        self.stdout.write(f'  ✓ تعداد استان‌ها: {province_count}')
        self.stdout.write(f'  ✓ تعداد شهرها: {city_count}')
        
        if city_count > 0:
            # نمونه شهرها
            self.stdout.write(f'\n📍 نمونه شهرها:')
            cities = City.objects.using('team4').select_related('province')[:5]
            for city in cities:
                location_str = f'({city.longitude}, {city.latitude})' if city.location else 'بدون موقعیت'
                self.stdout.write(f'  • {city.name_fa} - {city.province.name_fa} - {location_str}')
