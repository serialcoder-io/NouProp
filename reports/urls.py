from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path
from django.contrib import admin
from .views import reports, create_report

urlpatterns = [
    path("reports/", reports, name="reports"),
    path("create_report/", create_report, name="create_report"),
]