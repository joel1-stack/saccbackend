from django.contrib import admin
from .models import ReportSchedule


@admin.register(ReportSchedule)
class ReportScheduleAdmin(admin.ModelAdmin):
    list_display = ['name', 'report_type', 'frequency', 'is_active', 'last_generated', 'next_generation']
    list_filter = ['report_type', 'frequency', 'is_active']
    search_fields = ['name']
    readonly_fields = ['last_generated', 'created_at']