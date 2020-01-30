from django.contrib import admin
from .models import Network, Social_media, Gronner, Dedication
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

class GronnerInline(admin.StackedInline):
    model = Gronner
    can_delete = False
    verbose_name_plural = 'Gronners'

class UserAdmin(BaseUserAdmin):
    inlines = (GronnerInline,)

admin.site.register(Network)
admin.site.register(Social_media)
admin.site.register(Dedication)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
