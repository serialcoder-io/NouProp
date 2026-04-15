import uuid
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db.models import TextChoices
from django_quill.fields import QuillField
from django.db import models
from django.utils.text import slugify

from locations.models import Area
from users.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Listing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='listings', verbose_name='Category')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings', verbose_name='User')
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, blank=True, related_name='listings', verbose_name='Area')
    title = models.CharField(max_length=60)
    description = QuillField(blank=True, null=True)
    image = models.ImageField(upload_to='listings', blank=True, null=True, verbose_name='Image')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Created at')
    last_updated_at = models.DateTimeField(auto_now=True, verbose_name='Last updated at')
    is_open = models.BooleanField(default=True, verbose_name='Is Open')
    is_deleted = models.BooleanField(default=False, verbose_name='Is deleted')
    is_free= models.BooleanField(default=True, verbose_name='Is free')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )

    class Meta:
        db_table = 'listings'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_free']),
        ]

    def save(self, *args, **kwargs):
        if self.is_deleted:
            self.is_open = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class OfferStatus(TextChoices):
    PENDING = 'pending', 'Pending'
    ACCEPTED = 'accepted', 'Accepted'
    REJECTED = 'rejected', 'Rejected'

class Offer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers', verbose_name='User')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='offers', verbose_name='Listing')
    whatsapp_contact_allowed = models.BooleanField(default=False, verbose_name='Allow WhatsApp contact')
    whatsapp_number = PhoneNumberField(blank=True, null=True, verbose_name='WhatsApp number')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    last_updated_at = models.DateTimeField(auto_now=True, verbose_name='Last updated at')
    status = models.CharField(
        choices=OfferStatus.choices, # type: ignore
        default=OfferStatus.PENDING,
        max_length=10,
        db_index=True,
        verbose_name='Status'
    )
    message = QuillField(blank=True, null=True, verbose_name='Message')

    class Meta:
        db_table = 'offers'
        indexes = [
            models.Index(fields=['status']),
        ]

    def clean(self):
        super().clean()
        if self.listing_id and self.user_id:
            if self.user_id == self.listing.user_id:
                raise ValidationError("You cannot make an offer on your own listing.")

        if self.whatsapp_contact_allowed and not self.whatsapp_number:
            raise ValidationError("WhatsApp number is required if contact is allowed.")

        if not self.whatsapp_contact_allowed and self.whatsapp_number:
            raise ValidationError("WhatsApp number should be empty if contact is not allowed.")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        if not self.user_id or not self.listing_id:
            return f"Offer created at: {self.created_at}"
        return f"Offer by {self.user.email} on {self.listing.title}"

