# app/admin.py

from django.contrib import admin
from .models import DisasterReport


@admin.register(DisasterReport)
class DisasterReportAdmin(admin.ModelAdmin):
    list_display = ("latitude", "longitude", "reported_at")
    list_filter = ("reported_at",)
    search_fields = ("latitude", "longitude")
