#attendance/urls.py

from django.urls import path
from .views import StudentListCreateView, AttendanceListCreateView

urlpatterns = [
    path('students/', StudentListCreateView.as_view(), name='student-list-create'),
    path('attendance/', AttendanceListCreateView.as_view(), name='attendance-list-create'),
]
