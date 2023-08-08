from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

USER_TYPE = (
    ("Employer", "Employer"),
    ("Employee", "Employee"),  
)

SEX = (
    ("Male", "Male"),
    ("Female", "Female"),    
)

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    user_type = models.CharField(max_length=50, choices=USER_TYPE, default='Employer')
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        self.username = self.email
        super().save(*args, **kwargs)


class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employer_profile")

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

class Company(models.Model):
    name = models.CharField(max_length=50)
    employer = models.OneToOneField(EmployerProfile, on_delete=models.CASCADE, related_name="company")

    def __str__(self):
        return f'{self.name}'

class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee_profile")
    role = models.CharField(max_length=50, default='Employer')
    id_number = models.CharField(max_length=50)
    sex = models.CharField(max_length=10, choices=SEX)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="employees")

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
