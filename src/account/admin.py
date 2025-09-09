from django.contrib import admin

# Register your models here.
from account.models import UserModel

admin.site.register(UserModel)
