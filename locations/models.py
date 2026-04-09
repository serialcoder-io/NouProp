import uuid
from django.db import models
from django.utils.text import slugify

class District(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        db_table = 'districts'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Area(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    class Meta:
        db_table = 'areas'
        constraints = [
            models.UniqueConstraint(fields=['district', 'slug'], name='unique_area_per_district')
        ]
        indexes = [models.Index(fields=['district', 'slug']),]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


