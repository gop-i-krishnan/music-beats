from rest_framework import serializers
from .models import FeeRecord

class FeeRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()

    class Meta:
        model = FeeRecord
        fields = ['id', 'student', 'student_name', 'amount', 'date_paid', 'description']

    def get_student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"
