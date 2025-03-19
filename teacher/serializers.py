from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from teacher.models import Teacher


class TeacherModelSerializer(ModelSerializer):
    fullname = SerializerMethodField()
    subject = SerializerMethodField()

    class Meta:
        model = Teacher
        fields = 'fullname', 'email', 'subject', 'office_hours'

    def get_fullname(self, obj):
        return  obj.category + " " + obj.first_name + " " + obj.last_name

    def get_subject(self, obj):
        return obj.science.name
