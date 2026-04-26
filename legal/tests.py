from django.test import TestCase
from django.urls import reverse


class LegalPagesTests(TestCase):
    def test_terms_of_use_page_renders(self):
        response = self.client.get(reverse("terms_of_use"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Terms of Use")
        self.assertContains(response, "anliomar@outlook.com")

    def test_privacy_policy_page_renders(self):
        response = self.client.get(reverse("privacy_policy"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Privacy Policy")
        self.assertContains(response, "Data Protection Act 2017")

    def test_legal_notice_page_renders(self):
        response = self.client.get(reverse("legal_notice"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Legal Notice")
        self.assertContains(response, "+230 5848 3071")

    def test_home_page_contains_footer_legal_links(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse("terms_of_use"))
        self.assertContains(response, reverse("privacy_policy"))
        self.assertContains(response, reverse("legal_notice"))
