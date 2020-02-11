from django.contrib import admin
from .models import Gronner, Follow
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

class GronnerInline(admin.StackedInline):
    model = Gronner
    can_delete = False
    verbose_name_plural = 'Gronners'

class UserAdmin(BaseUserAdmin):
    inlines = (GronnerInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Follow)
