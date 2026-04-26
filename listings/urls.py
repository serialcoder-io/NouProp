from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path
from django.contrib import admin
from .views import listings_view, listing_details, make_offer, create_listing

urlpatterns = [
    path("", listings_view, name="listings"),
    path("create/", create_listing, name="create_listing"),
    path("<uuid:listing_id>/", listing_details, name="listing_details"),
    path("<uuid:listing_id>/make-offer/", make_offer, name="make_offer"),
]