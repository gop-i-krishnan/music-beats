# payments/views.py
# This code defines the views for handling fee records in a Django application.
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import FeeRecord
from .serializers import FeeRecordSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import FeeRecord
from django.db.models import Sum, Count
from datetime import datetime
    
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class FeeRecordListCreateView(generics.ListCreateAPIView):
    serializer_class = FeeRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = FeeRecord.objects.all()

        # --- Filtering logic ---
        student_id = self.request.query_params.get('student')
        min_amount = self.request.query_params.get('min_amount')
        max_amount = self.request.query_params.get('max_amount')
        date = self.request.query_params.get('date')

        if student_id:
            queryset = queryset.filter(student_id=student_id)
        if min_amount:
            queryset = queryset.filter(amount__gte=min_amount)
        if max_amount:
            queryset = queryset.filter(amount__lte=max_amount)
        if date:
            queryset = queryset.filter(date_paid=date)

        return queryset
    
class FeeSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id):
        start_date = request.query_params.get('start')
        end_date = request.query_params.get('end')

        filters = {'student_id': student_id}
        if start_date:
            filters['date_paid__gte'] = start_date
        if end_date:
            filters['date_paid__lte'] = end_date

        fees = FeeRecord.objects.filter(**filters)

        total_amount = fees.aggregate(Sum('amount'))['amount__sum'] or 0
        total_payments = fees.aggregate(Count('id'))['id__count']

        return Response({
            "student_id": student_id,
            "total_paid": total_amount,
            "total_payments": total_payments
        })

class FeeRecordRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FeeRecord.objects.all()
    serializer_class = FeeRecordSerializer
    permission_classes = [IsAuthenticated]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def overall_fee_summary(request):
    from .models import FeeRecord
    from django.db.models import Sum, Count

    total_amount = FeeRecord.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_transactions = FeeRecord.objects.aggregate(Count('id'))['id__count']

    return Response({
        "total_amount_received": total_amount,
        "total_number_of_payments": total_transactions
    })
