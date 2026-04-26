from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from allauth.socialaccount.models import SocialAccount
from listings.models import Category, Listing, Offer
from locations.models import Area, District
from reports.models import Report
from users.models import Role


class UserListingDetailsViewTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.owner = self.user_model.objects.create_user(
            email="owner@example.com",
            password="testpass123",
        )
        self.other_user = self.user_model.objects.create_user(
            email="other@example.com",
            password="testpass123",
        )
        self.offer_user = self.user_model.objects.create_user(
            email="offerer@example.com",
            password="testpass123",
        )

        self.category = Category.objects.create(name="Plastic")
        self.district = District.objects.create(name="Plaines Wilhems")
        self.area = Area.objects.create(name="Quatre Bornes", district=self.district)

        self.listing = Listing.objects.create(
            category=self.category,
            user=self.owner,
            area=self.area,
            title="Reusable bottles",
            description="Clean plastic bottles available.",
            is_free=True,
            price="0.00",
        )

    def test_listing_details_requires_login(self):
        response = self.client.get(reverse("user_listing_details", args=[self.listing.id]))

        self.assertEqual(response.status_code, 302)

    def test_listing_details_forbids_non_owner(self):
        self.client.force_login(self.other_user)

        response = self.client.get(reverse("user_listing_details", args=[self.listing.id]))

        self.assertEqual(response.status_code, 403)

    def test_listing_details_shows_owner_listing_and_offers(self):
        Offer.objects.create(
            user=self.offer_user,
            listing=self.listing,
            whatsapp_contact_allowed=True,
            whatsapp_number="+23052525252",
            status="pending",
            message="Can collect tomorrow.",
        )

        self.client.force_login(self.owner)
        response = self.client.get(reverse("user_listing_details", args=[self.listing.id]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["listing"], self.listing)
        self.assertEqual(len(response.context["offers"]), 1)
        self.assertContains(response, "Reusable bottles")
        self.assertContains(response, "offerer@example.com")

    def test_listing_details_paginate_offers(self):
        for index in range(11):
            Offer.objects.create(
                user=self.offer_user,
                listing=self.listing,
                status="pending",
                message=f"Offer message {index}",
            )

        self.client.force_login(self.owner)

        first_page = self.client.get(reverse("user_listing_details", args=[self.listing.id]))
        second_page = self.client.get(
            reverse("user_listing_details", args=[self.listing.id]),
            {"page": 2},
        )

        self.assertEqual(first_page.status_code, 200)
        self.assertEqual(second_page.status_code, 200)
        self.assertEqual(len(first_page.context["offers"]), 10)
        self.assertEqual(len(second_page.context["offers"]), 1)
        self.assertEqual(first_page.context["page_obj"].paginator.count, 11)


class UserOfferDetailsViewTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.owner = self.user_model.objects.create_user(
            email="owner@example.com",
            password="testpass123",
        )
        self.other_user = self.user_model.objects.create_user(
            email="other@example.com",
            password="testpass123",
        )
        self.offer_user = self.user_model.objects.create_user(
            email="offerer@example.com",
            password="testpass123",
        )
        self.second_offer_user = self.user_model.objects.create_user(
            email="offerer2@example.com",
            password="testpass123",
        )

        self.category = Category.objects.create(name="Metal")
        self.district = District.objects.create(name="Moka")
        self.area = Area.objects.create(name="Helvetia", district=self.district)
        self.listing = Listing.objects.create(
            category=self.category,
            user=self.owner,
            area=self.area,
            title="Metal cans",
            description="Sorted and ready.",
            is_free=True,
            price="0.00",
        )
        self.offer = Offer.objects.create(
            user=self.offer_user,
            listing=self.listing,
            whatsapp_contact_allowed=True,
            whatsapp_number="+23057575757",
            status="pending",
            message="I can pick these up today.",
        )

    def test_offer_details_requires_login(self):
        response = self.client.get(reverse("offer_details", args=[self.offer.id]))

        self.assertEqual(response.status_code, 302)

    def test_offer_details_forbids_unrelated_user(self):
        self.client.force_login(self.other_user)

        response = self.client.get(reverse("offer_details", args=[self.offer.id]))

        self.assertEqual(response.status_code, 403)

    def test_offer_creator_can_view_offer_details(self):
        self.client.force_login(self.offer_user)

        response = self.client.get(reverse("offer_details", args=[self.offer.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "I can pick these up today.")
        self.assertNotContains(response, "Confirm Accept")

    def test_listing_owner_can_accept_offer_and_close_listing(self):
        other_offer = Offer.objects.create(
            user=self.second_offer_user,
            listing=self.listing,
            status="pending",
            message="Backup offer",
        )

        self.client.force_login(self.owner)
        response = self.client.post(
            reverse("offer_details", args=[self.offer.id]),
            {"action": "accept"},
        )

        self.offer.refresh_from_db()
        other_offer.refresh_from_db()
        self.listing.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.offer.status, "accepted")
        self.assertEqual(other_offer.status, "rejected")
        self.assertFalse(self.listing.is_open)

    def test_listing_owner_can_reject_offer(self):
        self.client.force_login(self.owner)
        response = self.client.post(
            reverse("offer_details", args=[self.offer.id]),
            {"action": "reject"},
        )

        self.offer.refresh_from_db()
        self.listing.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.offer.status, "rejected")
        self.assertTrue(self.listing.is_open)

    def test_offer_creator_cannot_accept_or_reject(self):
        self.client.force_login(self.offer_user)

        response = self.client.post(
            reverse("offer_details", args=[self.offer.id]),
            {"action": "accept"},
        )

        self.offer.refresh_from_db()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.offer.status, "pending")

    def test_processed_offer_message_is_displayed(self):
        self.offer.status = "accepted"
        self.offer.save()
        self.client.force_login(self.owner)

        response = self.client.get(reverse("offer_details", args=[self.offer.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You already accepted this offer.")

    def test_delete_offer_soft_deletes_for_creator(self):
        self.client.force_login(self.offer_user)

        response = self.client.post(reverse("delete_offer", args=[self.offer.id]))

        self.offer.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.offer.is_deleted)

    def test_delete_offer_forbids_non_creator(self):
        self.client.force_login(self.owner)

        response = self.client.post(reverse("delete_offer", args=[self.offer.id]))

        self.offer.refresh_from_db()

        self.assertEqual(response.status_code, 403)
        self.assertFalse(self.offer.is_deleted)


class AccountManagementViewTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.citizen_role = Role.objects.create(name="citizen")
        self.collector_role = Role.objects.create(name="collector")

        self.user = self.user_model.objects.create_user(
            email="account@example.com",
            password="testpass123",
            display_name="Account User",
            whatsapp_number="+23058000000",
            role=self.collector_role,
        )
        self.other_user = self.user_model.objects.create_user(
            email="other-account@example.com",
            password="testpass123",
            role=self.citizen_role,
        )

        self.category = Category.objects.create(name="Glass")
        self.district = District.objects.create(name="Riviere du Rempart")
        self.area = Area.objects.create(name="Goodlands", district=self.district)

        self.listing = Listing.objects.create(
            category=self.category,
            user=self.user,
            area=self.area,
            title="Glass jars",
            is_free=True,
            price="0.00",
        )
        self.offer = Offer.objects.create(
            user=self.user,
            listing=self.listing,
            status="pending",
            message="Interested in a trade.",
        )
        self.report = Report.objects.create(
            user=self.user,
            area=self.area,
            title="Overflowing waste point",
            status="pending",
        )

    def test_account_pages_require_login(self):
        for url_name in (
            "account_overview",
            "edit_account",
            "account_data_management",
            "delete_account",
        ):
            response = self.client.get(reverse(url_name))
            self.assertEqual(response.status_code, 302)

    def test_account_overview_shows_custom_user_fields(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("account_overview"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "account@example.com")
        self.assertContains(response, "Account User")
        self.assertContains(response, "collector")

    def test_edit_account_updates_custom_user_fields(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("edit_account"),
            {
                "email": "updated-account@example.com",
                "display_name": "Updated Name",
                "whatsapp_number": "+23058111111",
            },
        )

        self.user.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.email, "updated-account@example.com")
        self.assertEqual(self.user.display_name, "Updated Name")
        self.assertEqual(str(self.user.whatsapp_number), "+23058111111")

    def test_edit_account_shows_locked_email_for_social_account(self):
        SocialAccount.objects.create(
            user=self.user,
            provider="google",
            uid="google-account-1",
            extra_data={},
        )
        self.client.force_login(self.user)

        response = self.client.get(reverse("edit_account"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Email cannot be changed for social login accounts")
        self.assertContains(response, "disabled")

    def test_edit_account_does_not_update_email_for_social_account(self):
        SocialAccount.objects.create(
            user=self.user,
            provider="google",
            uid="google-account-2",
            extra_data={},
        )
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("edit_account"),
            {
                "email": "hijack@example.com",
                "display_name": "Social Name",
                "whatsapp_number": "+23058222222",
            },
        )

        self.user.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.email, "account@example.com")
        self.assertEqual(self.user.display_name, "Social Name")
        self.assertEqual(str(self.user.whatsapp_number), "+23058222222")

    def test_account_data_management_lists_related_content(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("account_data_management"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Glass jars")
        self.assertContains(response, "Offers")
        self.assertContains(response, "Overflowing waste point")

    def test_delete_account_requires_matching_confirmation_email(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("delete_account"),
            {"confirmation_email": "wrong@example.com"},
        )

        self.user.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.is_active)
        self.assertContains(response, "Enter your current account email to confirm deletion.")

    def test_delete_account_deactivates_and_logs_out_user(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("delete_account"),
            {"confirmation_email": "account@example.com"},
        )

        self.user.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.user.is_active)
        self.assertNotIn("_auth_user_id", self.client.session)
