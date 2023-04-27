from django import forms
from django.contrib import admin
from django.contrib.auth import password_validation
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from users.models import Follow, FoodgramUser


class FoodgramUserCreationForm(forms.ModelForm):
    password = forms.CharField(
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )

    class Meta:
        model = FoodgramUser
        fields = ('username',)
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        username_field = self._meta.model.USERNAME_FIELD
        if username_field in self.fields:
            self.fields[username_field].widget.attrs['autofocus'] = True

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


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
        'password',
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
    add_form = FoodgramUserCreationForm


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'author']


admin.site.unregister(Group)
