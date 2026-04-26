from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from listings.models import Category, Listing, Offer
from locations.models import Area, District


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
        self.assertContains(response, "Can collect tomorrow.")

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
