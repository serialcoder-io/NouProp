from django.urls import path

from .views import legal_notice, privacy_policy, terms_of_use


urlpatterns = [
    path("terms-of-use/", terms_of_use, name="terms_of_use"),
    path("privacy-policy/", privacy_policy, name="privacy_policy"),
    path("legal-notice/", legal_notice, name="legal_notice"),
]
