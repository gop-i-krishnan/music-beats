# payments/models.py
from django.db import models
from accounts.models import CustomUser  # for linking students

class FeeRecord(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.student.email} - ₹{self.amount}"
