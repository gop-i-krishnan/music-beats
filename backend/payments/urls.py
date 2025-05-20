# payments/urls.py
# This code defines the URL patterns for the payments app in a Django project.
from django.urls import path
from .views import FeeRecordListCreateView, FeeSummaryView, FeeRecordRetrieveUpdateDestroyView, overall_fee_summary


urlpatterns = [
    path('fees/', FeeRecordListCreateView.as_view(), name='fee-list-create'),
    path('fees/<int:pk>/', FeeRecordRetrieveUpdateDestroyView.as_view(), name='fee-detail'),
    path('fees/<int:student_id>/summary/', FeeSummaryView.as_view(), name='fee-summary'),
    path('fees/summary/overall/', overall_fee_summary, name='fee-overall-summary'),
]
