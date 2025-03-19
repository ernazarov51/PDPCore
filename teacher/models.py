from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.db.models import TextChoices, ForeignKey, SET_NULL, CharField


# Create your models here.
class Teacher(AbstractUser):
    groups = models.ManyToManyField(Group, related_name="teacher_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="teacher_permissions_set")
    class CategoryChoices(TextChoices):
        doctor = 'doctor', 'Doctor'
        professor = 'professor', 'Professor'

    science = ForeignKey('apps.Science', on_delete=SET_NULL, related_name='teachers',null=True)
    office_hours = CharField(max_length=250, null=True, blank=True)
    category = CharField(max_length=250, choices=CategoryChoices.choices)

    def __str__(self):
        return self.category + " " + self.first_name + " " + self.last_name

