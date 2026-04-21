from django.core.management.base import BaseCommand
from reports.models import Tag

class Command(BaseCommand):
    help = "Seed initial tags"

    def handle(self, *args, **kwargs):
        tags = [
            "plastic", "metal", "glass", "paper", "cardboard",
            "organic", "electronic", "battery", "chemical",
            "bulky", "furniture", "mattress", "appliance",
            "construction", "rubble",
            "hazardous", "toxic", "flammable", "medical",
            "roadside", "river", "beach", "forest",
            "public_area", "private_land",
            "recent", "old", "spreading", "burned"
        ]

        for tag_name in tags:
            Tag.objects.get_or_create(name=tag_name)

        self.stdout.write(self.style.SUCCESS("Tags inserted successfully"))