from django.contrib import admin

from apps.models import User, Science, UserScience

admin.site.register(User)
admin.site.register(Science)
admin.site.register(UserScience)
