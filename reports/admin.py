from django.contrib import admin
from .models import Report, Tag

class ReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'lat', 'lng', 'created_at']

class TagAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Report, ReportAdmin)
admin.site.register(Tag, TagAdmin)