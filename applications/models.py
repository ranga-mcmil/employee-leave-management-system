from django.db import models
from accounts.models import EmployeeProfile, Company
from django.utils import timezone

STATUS = (
    ("Pending", "Pending"),
    ("Declined", "Declined"),
    ("Approved", "Approved"),    
)

# Create your models here.
class Application(models.Model):
    status = models.CharField(max_length=50, choices=STATUS, default="Pending")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name="applications")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="applications")
    date_created = models.DateTimeField(auto_now_add=True)

    def get_remaining_days(self):
        if self.status != 'Approved':
            return '\'\''

        if timezone.now() < self.start_date:
            return 'Leave hasnt started'

        if timezone.now() > self.end_date:
            return 'Leave has expired'

        return f'{(self.end_date - self.start_date).days}'