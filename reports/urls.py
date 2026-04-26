from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path
from django.contrib import admin
from .views import reports, create_report, report_details, staff_reports_list

urlpatterns = [
    path("reports/", reports, name="reports"),
    path("create_report/", create_report, name="create_report"),
    path("staff_reports/", staff_reports_list, name="staff_reports_list"),
    path("<uuid:report_id>/", report_details, name="report_details"),
]
