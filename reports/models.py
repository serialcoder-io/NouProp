import uuid

from django.db import models
from django.utils.text import slugify
from django_quill.fields import QuillField
from locations.models import Area
from users.models import User


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    name = models.CharField(max_length=50, verbose_name='Tag', unique=True)
    slug = models.SlugField(blank=True, verbose_name='Slug', unique=True)
    color = models.CharField(max_length=20, verbose_name='Color', null=True, blank=True)
    def __str__(self):
        return self.name
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ReportStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    VALIDATED = "validated", "Validated"
    IN_PROGRESS = "in_progress", "In Progress"
    COMPLETED = "completed", "Completed"
    REJECTED = "rejected", "Rejected"

class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='reports',
        verbose_name='User',
    )
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports', verbose_name='Area')
    tags = models.ManyToManyField(Tag, blank=True)
    title = models.CharField(max_length=100, verbose_name='Title')
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    status = models.CharField(
        choices=ReportStatus.choices, # type: ignore
        default=ReportStatus.PENDING,
        max_length=20,
        verbose_name='Status'
    )
    lat = models.FloatField(blank=True, null=True, verbose_name='Latitude')
    lng = models.FloatField(blank=True, null=True, verbose_name='Longitude')
    address = models.TextField(blank=True, null=True, verbose_name='Address')
    image = models.ImageField(upload_to='listings', blank=True, null=True, verbose_name='Image')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='Updated at')

    def __str__(self):
        return self.title or str(self.id)
