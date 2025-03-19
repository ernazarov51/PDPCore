from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from apps.models import User, Science, UserScience, Task, TaskResult


class TaskSerializer(ModelSerializer):
    user_earned=SerializerMethodField()
    class Meta:
        model = Task
        fields='title','total','user_earned'

    def get_user_earned(self, obj):
        task_result = TaskResult.objects.filter(task=obj).first()
        return task_result.user_earned if task_result and task_result.user_earned else None


class ScienceSerializer(ModelSerializer):
    rank=SerializerMethodField()
    percentage = SerializerMethodField()
    tasks = SerializerMethodField()

    class Meta:
        model = Science
        fields = 'name','rank','percentage','tasks'


    def get_rank(self, obj):
        return 0

    def get_percentage(self, obj):
        return 0

    def get_tasks(self, obj):
        return TaskSerializer(obj.tasks.all(),many=True).data






class UserDetailSerializer(ModelSerializer):
    full_name = SerializerMethodField()
    sciences = SerializerMethodField()

    class Meta:
        model = User
        fields = 'avatar', 'full_name', 'gpa', 'sciences'

    def get_full_name(self, obj):
        return obj.first_name + ' ' + obj.last_name
    def get_sciences(self, obj):
        sciences=Science.objects.filter(users__user=obj)
        return ScienceSerializer(sciences, many=True).data

