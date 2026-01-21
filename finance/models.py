from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email: raise ValueError('Email shart')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

class EmailOTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    def is_valid(self):
        now = timezone.now()
        diff = (now - self.created_at).total_seconds()
        return diff < 300

class Currency(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=3)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self): return self.code

class Source(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self): return self.name

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    def __str__(self):
        return f"{self.name} ({self.balance} {self.currency.code})"

class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='category_icons/', blank=True, null=True)
    def __str__(self): return self.name

class Transaction(models.Model):
    TRANSACTION_TYPES = (('income', 'Kirim'), ('expense', 'Chiqim'),)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True)
    def __str__(self): return f"{self.type} - {self.amount}"