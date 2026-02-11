from django.contrib import admin

from .models import Trip


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    """مدیریت سفرها در پنل ادمین"""
    model = Trip
    ordering = ("-created_at",)
    list_display = ("destination_name", "origin_name", "days", "status", "user", "created_at")
    search_fields = ("destination_name", "origin_name", "user__email")
    list_filter = ("status", "created_at")

    fieldsets = (
        ("اطلاعات مسیر", {"fields": ("user", "destination_name", "origin_name")}),
        ("جزئیات سفر", {"fields": ("days", "people", "start_at", "styles")}),
        ("هزینه‌ها", {"fields": ("budget", "total_cost")}),
        ("وضعیت", {"fields": ("status",)}),
        ("تاریخچه", {"fields": ("created_at", "updated_at")}),
    )

    readonly_fields = ("created_at", "updated_at")