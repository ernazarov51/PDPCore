from django.shortcuts import render
from django.views.generic import TemplateView
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.models import User
from apps.serializers import UserDetailSerializer


class WebsocketTemplateView(TemplateView):
    template_name = 'apps/index.html'


@extend_schema(tags=['Student Detail'])
@api_view(['GET'])
def student_detail_apiview(request,pk):
    user=User.objects.filter(pk=pk).first()
    serializer=UserDetailSerializer(user)
    return Response(serializer.data)
