from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path
from django.contrib import admin
from .views import listings_view, listing_details

urlpatterns = [
    path("", listings_view, name="listings"),
    path("<uuid:listing_id>/", listing_details, name="listing_details"),
]