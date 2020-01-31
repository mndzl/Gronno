from django.contrib import admin
from .models import Category, Project, Medal, Comment, Award

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'author', 'category')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'diminutive')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'text')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Medal)
admin.site.register(Award)




