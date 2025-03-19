
from django.urls import path

from apps.views import WebsocketTemplateView, student_detail_apiview

urlpatterns = [
    path('', WebsocketTemplateView.as_view(),name='websocket' ),
    path('api/v1/student_detail/<int:pk>/', student_detail_apiview ),
]
