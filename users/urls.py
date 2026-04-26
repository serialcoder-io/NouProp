# from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path
from django.contrib import admin
from .views import (
    account_data_management,
    account_overview,
    delete_account,
    edit_account,
    my_listings,
    listing_details,
    offer_details,
    my_offers,
    received_offers,
    my_reports,
    edit_listing,
    delete_offer,
    delete_listing,
)

urlpatterns = [
    path("account/", account_overview, name="account_overview"),
    path("account/edit/", edit_account, name="edit_account"),
    path("account/data/", account_data_management, name="account_data_management"),
    path("account/delete/", delete_account, name="delete_account"),
    path("my_listings/", my_listings, name="my_listings"),
    path("listings/<uuid:listing_id>/", listing_details, name="user_listing_details"),
    path("offers/<uuid:offer_id>/", offer_details, name="offer_details"),
    path("offers/<uuid:offer_id>/delete/", delete_offer, name="delete_offer"),
    path("my_offers/", my_offers, name="my_offers"),
    path("received_offers/", received_offers, name="received_offers"),
    path("my_reports/", my_reports, name="my_reports"),
    path("listings/<uuid:listing_id>/edit/", edit_listing, name="edit_listing"),
    path("listings/<uuid:listing_id>/delete/", delete_listing, name="delete_listing"),
]
