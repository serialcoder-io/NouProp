from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

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


class StaffReportsListViewTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.staff_user = self.user_model.objects.create_user(
            email="staff-list@example.com",
            password="testpass123",
            is_staff=True,
        )
        self.normal_user = self.user_model.objects.create_user(
            email="normal@example.com",
            password="testpass123",
        )
        self.report_user = self.user_model.objects.create_user(
            email="report-user@example.com",
            password="testpass123",
        )

        self.district = District.objects.create(name="Plaines Wilhems")
        self.area_one = Area.objects.create(name="Curepipe", district=self.district)
        self.area_two = Area.objects.create(name="Vacoas", district=self.district)
        self.tag_plastic = Tag.objects.create(name="Plastic Waste", color="#22c55e")
        self.tag_hazard = Tag.objects.create(name="Hazardous")

        self.report_one = Report.objects.create(
            user=self.report_user,
            area=self.area_one,
            title="Plastic bottles near river",
            description="Riverbank dumping.",
            status="pending",
            address="River Road",
        )
        self.report_one.tags.add(self.tag_plastic)

        self.report_two = Report.objects.create(
            user=self.report_user,
            area=self.area_two,
            title="Construction debris",
            description="Broken concrete blocks.",
            status="completed",
            address="Main Road",
        )
        self.report_two.tags.add(self.tag_hazard)

        Report.objects.filter(pk=self.report_one.pk).update(
            created_at=timezone.now() - timedelta(days=5)
        )
        Report.objects.filter(pk=self.report_two.pk).update(
            created_at=timezone.now() - timedelta(hours=12)
        )
        self.report_one.refresh_from_db()
        self.report_two.refresh_from_db()

    def test_staff_reports_list_forbids_non_staff(self):
        self.client.force_login(self.normal_user)

        response = self.client.get(reverse("staff_reports_list"))

        self.assertEqual(response.status_code, 403)

    def test_staff_reports_list_allows_staff(self):
        self.client.force_login(self.staff_user)

        response = self.client.get(reverse("staff_reports_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Reports Management")
        self.assertContains(response, "Plastic bottles near river")
        self.assertContains(response, "Construction debris")

    def test_staff_reports_list_filters_by_search_status_area_and_tags(self):
        self.client.force_login(self.staff_user)

        response = self.client.get(
            reverse("staff_reports_list"),
            {
                "q": "Plastic",
                "status": "pending",
                "area": str(self.area_one.id),
                "tag": str(self.tag_plastic.id),
            },
        )

        reports = list(response.context["reports"])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(reports, [self.report_one])

    def test_staff_reports_list_filters_by_date_filter(self):
        self.client.force_login(self.staff_user)

        response = self.client.get(
            reverse("staff_reports_list"),
            {
                "date_filter": "1",
            },
        )

        reports = list(response.context["reports"])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(reports, [self.report_two])

    def test_staff_reports_list_paginates_and_preserves_query_params(self):
        for index in range(10):
            report = Report.objects.create(
                user=self.report_user,
                area=self.area_one,
                title=f"Overflow report {index}",
                status="pending",
            )
            report.tags.add(self.tag_plastic)

        self.client.force_login(self.staff_user)

        response = self.client.get(
            reverse("staff_reports_list"),
            {
                "status": "pending",
                "tag": str(self.tag_plastic.id),
                "page": 2,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page_obj"].number, 2)
        self.assertIn("status=pending", response.context["query_params"])
        self.assertIn("tag=", response.context["query_params"])

    def test_staff_reports_list_returns_partial_for_htmx_results_target(self):
        self.client.force_login(self.staff_user)

        response = self.client.get(
            reverse("staff_reports_list"),
            HTTP_HX_REQUEST="true",
            HTTP_HX_TARGET="staff-reports",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Report Results")
        self.assertNotContains(response, "<html", html=False)
