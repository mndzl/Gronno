from django.contrib import admin
from .models import (
    Category, 
    Project, 
    Medal,
    Comment, 
    Award,
    Report,
)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'author', 'category', 'points', 'is_active')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'diminutive')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'text')

class ReportAdmin(admin.ModelAdmin):
    list_display = ('project', 'reason', 'user')



admin.site.register(Category, CategoryAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Medal)
admin.site.register(Award)



