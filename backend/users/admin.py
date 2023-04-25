from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import Follow, FoodgramUser

admin.site.register(FoodgramUser, UserAdmin)
admin.site.register(Follow)
