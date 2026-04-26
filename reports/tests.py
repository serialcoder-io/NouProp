from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from locations.models import Area, District

from .models import Report, Tag


class ReportDetailsViewTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.owner = self.user_model.objects.create_user(
            email="reporter@example.com",
            password="testpass123",
        )
        self.staff_user = self.user_model.objects.create_user(
            email="staff@example.com",
            password="testpass123",
            is_staff=True,
        )
        self.other_user = self.user_model.objects.create_user(
            email="other@example.com",
            password="testpass123",
        )

        self.district = District.objects.create(name="Moka")
        self.area = Area.objects.create(name="Belle Rose", district=self.district)
        self.tag_one = Tag.objects.create(name="Plastic", color="#22c55e")
        self.tag_two = Tag.objects.create(name="Hazard")

        self.report = Report.objects.create(
            user=self.owner,
            area=self.area,
            title="Illegal dumping near canal",
            description="Several bags have been left near the roadside.",
            status="pending",
            lat=-20.233123,
            lng=57.496789,
            address="Canal Road, Belle Rose",
        )
        self.report.tags.add(self.tag_one, self.tag_two)

    def test_report_details_forbids_anonymous_user(self):
        response = self.client.get(reverse("report_details", args=[self.report.id]))

        self.assertEqual(response.status_code, 403)

    def test_report_owner_can_view_report_details(self):
        self.client.force_login(self.owner)

        response = self.client.get(reverse("report_details", args=[self.report.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Illegal dumping near canal")
        self.assertContains(response, "Belle Rose (Moka)")
        self.assertContains(response, "Plastic")
        self.assertContains(response, "Hazard")
        self.assertContains(response, 'id="report-map"', html=False)

    def test_staff_user_can_view_report_details(self):
        self.client.force_login(self.staff_user)

        response = self.client.get(reverse("report_details", args=[self.report.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Save Status")

    def test_unrelated_user_is_forbidden(self):
        self.client.force_login(self.other_user)

        response = self.client.get(reverse("report_details", args=[self.report.id]))

        self.assertEqual(response.status_code, 403)

    def test_staff_user_can_update_status(self):
        self.client.force_login(self.staff_user)

        response = self.client.post(
            reverse("report_details", args=[self.report.id]),
            {"status": "completed"},
        )

        self.report.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.report.status, "completed")

    def test_owner_cannot_update_status(self):
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse("report_details", args=[self.report.id]),
            {"status": "completed"},
        )

        self.report.refresh_from_db()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.report.status, "pending")
