from django.contrib.auth.models import AbstractUser
from django.db import models


class FoodgramUser(AbstractUser):
    class Meta():
        swappable = 'AUTH_USER_MODEL'