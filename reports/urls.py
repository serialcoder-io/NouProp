from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path
from django.contrib import admin
from .views import reports

urlpatterns = [
    path("reports/", reports, name="reports"),
]