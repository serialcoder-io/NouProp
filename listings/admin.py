from django.contrib import admin

from django.contrib import admin
from .models import Category, Listing, Offer

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'category__name', 'is_open', 'is_deleted', 'is_free', 'price'] # type: ignore

class OfferAdmin(admin.ModelAdmin):
    list_display = ['user__email', 'status', 'created_at']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Offer, OfferAdmin)