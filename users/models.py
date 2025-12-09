
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from .enums import RoleChoices


# -----------------------------
# Custom User Manager
# -----------------------------
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, role=RoleChoices.USER, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)

        # If dealer, start unapproved
        if role == RoleChoices.DEALER:
            user.is_approved = False
        else:
            user.is_approved = True  # other roles approved by default

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', RoleChoices.SUPER_ADMIN)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_approved', True)  # Super Admin approved by default

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


# -----------------------------
# Custom User Model
# -----------------------------
class User(AbstractBaseUser, PermissionsMixin):
    # Basic fields
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    # Role & workflow
    role = models.CharField(max_length=20, choices=RoleChoices.choices, default=RoleChoices.USER)
    is_approved = models.BooleanField(default=False)  # Only for Dealers

    # Permissions
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Timestamps
    date_joined = models.DateTimeField(default=timezone.now)

    # Groups & permissions related names
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='accounts_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='accounts_user_permissions_set',
        blank=True
    )

    # Manager
    objects = UserManager()

    # Email login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f"{self.email} ({self.role})"

    # Optional helpers
    @property
    def is_dealer(self):
        return self.role == RoleChoices.DEALER

    @property
    def is_superadmin(self):
        return self.role == RoleChoices.SUPER_ADMIN

    @property
    def is_user(self):
        return self.role == RoleChoices.USER
