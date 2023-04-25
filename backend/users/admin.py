from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from users.models import Follow, FoodgramUser


@admin.register(FoodgramUser)
class FoodgramUserAdmin(UserAdmin):
    search_fields = ['username', 'email', 'first_name']
    list_display = ['id', 'username', 'first_name', 'last_name', 'email']
    list_filter = ['username', 'email']
    fieldsets = [
        (
            _('Personal info'),
            {'fields': ['username', 'first_name', 'last_name', 'email']}
        ),
    ]
    add_field = [
        'username',
        'password1',
        'password2',
        'first_name',
        'last_name',
        'email'
    ]
    add_fieldsets = [
        (None, {
            'classes': ['wide'],
            'fields': add_field,
        })
    ]


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'author']


admin.site.unregister(Group)
