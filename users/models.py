from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group, Permission
)
from django.utils.translation import gettext_lazy as _
import uuid
from django.contrib.auth.models import User

class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)

        if not extra_fields.get('display_name'):
            extra_fields['display_name'] = email.split('@')[0]

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError(_('Superuser must have is_staff=True.'))
        if not extra_fields.get('is_superuser'):
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_('ID'))
    email = models.EmailField(verbose_name=_('email address'), unique=True)
    display_name = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(verbose_name=_('active'), default=True)
    is_staff = models.BooleanField(verbose_name=_('staff status'), default=False)
    date_joined = models.DateTimeField(verbose_name=_('date joined'), auto_now_add=True)

    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True, verbose_name=_('user groups'))
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
        verbose_name=_('user permissions')
    )
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, blank=True, null=True, related_name='customuser_set')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def save(self, *args, **kwargs):
        if not self.display_name and self.email:
            self.display_name = self.email.split('@')[0]

        if not self.role:
            self.role = Role.objects.filter(name='citizen').first()

        super().save(*args, **kwargs)

        if not self.role:
            self.role = Role.objects.filter(name='citizen').first()

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users'