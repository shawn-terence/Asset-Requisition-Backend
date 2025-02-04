from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from cloudinary.models import CloudinaryField

class CustomUserManager(BaseUserManager):
    def create_user(
        self,
        email,
        first_name,
        last_name,
        phone_number,
        department,
        role,
        password=None,
        **extra_fields
    ):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        username = email

        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            department=department,
            role=role,
            **extra_fields
        )

        if password:
            user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, first_name, last_name, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(
            email, first_name, last_name, password=password, **extra_fields
        )

class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("employee", "Employee"),
        ("superadmin", "SuperAdmin"),
    )

    profile_picture = CloudinaryField("image", blank=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=30,
    )
    department = models.CharField(max_length=30)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default="employee")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone_number", "department", "role"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

class Asset(models.Model):
    image = CloudinaryField("image", blank=True)
    name = models.CharField(max_length=30)
    description = models.TextField()
    category = models.CharField(max_length=30)
    serial_number = models.CharField(max_length=100, unique=True)
    tag = models.CharField(max_length=50)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    link = models.URLField(max_length=200, blank=True)
    owner = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='owned_assets',
        help_text="The user who owns the asset once the request is approved."
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Asset"
        verbose_name_plural = "Assets"

class Request(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    RETURN_STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("returned", "Returned"),
    )

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="requests")
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requests")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="pending")
    return_status = models.CharField(
        max_length=30,
        choices=RETURN_STATUS_CHOICES,
        default=None,
        blank=True,
        null=True,
        help_text="Status of the asset return request (if applicable)."
    )
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Request #{self.id} - {self.asset.name} ({self.status})"

    class Meta:
        verbose_name = "Request"
        verbose_name_plural = "Requests"