from django.urls import path

from teacher import views

urlpatterns=[
    path('api/v1/teachers/',views.get_teachers_apiview,name='home'),
]