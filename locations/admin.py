from django.contrib import admin

from django.contrib import admin
from .models import District, Area

class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name']

class AreaAdmin(admin.ModelAdmin):
    list_display = ['name', 'district__name']  # type: ignore

admin.site.register(District, DistrictAdmin)
admin.site.register(Area, AreaAdmin)