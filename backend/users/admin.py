from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import FoodgramUser, Follow

admin.site.register(FoodgramUser, UserAdmin)
admin.site.register(Follow)
