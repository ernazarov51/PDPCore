from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from teacher.models import Teacher
from teacher.serializers import TeacherModelSerializer


# Create your views here.
@extend_schema(tags=['Teacher'])
@api_view(['GET'])
def get_teachers_apiview(request):
    teachers=Teacher.objects.all()
    serializer=TeacherModelSerializer(teachers,many=True)
    return Response(serializer.data)