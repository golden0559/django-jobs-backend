from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)


class Employee(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    phone_number = models.CharField(max_length=15)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    city_name = models.CharField(max_length=100, blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  # Latitude field
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  # Longitude field

class Employer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    vat_number = models.CharField(max_length=30)
    company_name = models.CharField(max_length=100)
    street_name = models.CharField(max_length=100)
    house_number = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    coordinates = models.JSONField()  # Stores latitude and longitude as JSON
    website = models.URLField(blank=True, null=True)
    biography = models.TextField(blank=True, null=True)


class Admin(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)


class Review(models.Model):
    REVIEWER_TYPE_CHOICES = [
        ('employee', 'Employee'),
        ('employer', 'Employer'),
        ('anonymous', 'Anonymous'),  # For anonymous reviews
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True,
                                 related_name='employee_reviews')
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, null=True, blank=True,
                                 related_name='employer_reviews')
    anonymous_name = models.CharField(max_length=100, blank=True,
                                      null=True)  # Optional name field for anonymous reviews
    rating = models.PositiveIntegerField()  # Example: 1 to 5 stars
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewer_type = models.CharField(max_length=10, choices=REVIEWER_TYPE_CHOICES, default='anonymous')
