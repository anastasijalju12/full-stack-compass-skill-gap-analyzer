"""
Author: Sofija Nikolic, index: 2023/0603

Models for the accounts app: users, companies, administrators,
subscriptions, and password reset tokens.
"""

from decimal import Decimal

from django.db import models
from django.db.models.functions import Now


class User(models.Model):
    """Represents a user (a person looking for a job) in the system.

    Mapped to the existing 'user' table in the database. The 'role'
    field distinguishes regular users ('user') from administrators
    ('admin').
    """

    STATUS_CHOICES = [
        ('active', 'active'),
        ('pending', 'pending'),
    ]
    ROLE_CHOICES = [
        ('user', 'user'),
        ('admin', 'admin'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(unique=True, max_length=100)
    email = models.CharField(unique=True, max_length=150)
    password = models.CharField(max_length=255)
    contact = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, blank=True, null=True, db_default='pending')
    role = models.CharField(max_length=5, choices=ROLE_CHOICES, blank=True, null=True, db_default='user')
    registered_at = models.DateTimeField(blank=True, null=True, db_default=Now())
    rejection_reason = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user'


class Company(models.Model):
    """Represents a company (employer) in the system.

    Mapped to the existing 'company' table in the database.
    Newly registered companies get the 'pending' status until an
    administrator approves them.
    """

    STATUS_CHOICES = [
        ('active', 'active'),
        ('pending', 'pending'),
        ('rejected', 'rejected'),
    ]

    name = models.CharField(max_length=150)
    username = models.CharField(unique=True, max_length=100)
    email = models.CharField(unique=True, max_length=150, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    industry = models.CharField(max_length=150, blank=True, null=True)
    contact = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    logo_path = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, blank=True, null=True, db_default='pending')
    rejection_reason = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'company'


class Administrator(models.Model):
    """Additional information about a user who has the administrator role.

    Linked to the User model via FK; stores the access level and the
    date the administrator role was assigned.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_level = models.CharField(max_length=50, blank=True, null=True)
    assigned_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'administrator'


class Subscription(models.Model):
    """Represents a single subscription transaction for a user or company.

    Exactly one of the 'user'/'company' fields is populated, depending
    on who is subscribing. The status tracks the outcome of the payment.
    """

    STATUS_CHOICES = [
        ('success', 'success'),
        ('failed', 'failed'),
        ('cancelled', 'cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2, db_default=Decimal('10.00'))
    status = models.CharField(max_length=9, choices=STATUS_CHOICES)
    date = models.DateTimeField(db_default=Now())

    class Meta:
        managed = True
        db_table = 'subscription'


class PasswordReset(models.Model):
    """A password reset token, linked to a user or a company.

    The token has an expiration date (expires_at) and a flag marking
    whether it has already been used (is_used), to prevent reuse.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    token = models.CharField(unique=True, max_length=255)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(blank=True, null=True, db_default=False)

    class Meta:
        managed = True
        db_table = 'password_reset'
