# from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path
from django.contrib import admin
from .views import my_listings, my_offers, received_offers, my_reports

urlpatterns = [
    path("my_listings/", my_listings, name="my_listings"),
    path("my_offers/", my_offers, name="my_offers"),
    path("received_offers/", received_offers, name="received_offers"),
    path("my_reports/", my_reports, name="my_reports"),
]