# attendance/models.py

from django.db import models
from accounts.models import CustomUser  # using our custom user model

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    enrolled_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.full_name


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.student.user.full_name} - {self.date} - {self.status}"
