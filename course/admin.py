from django.contrib import admin
from .models import (
    Subject, Course, Module, Topic,
    Text, Video, Image, File, Comment
)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'owner', 'created']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course']


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['module', 'content_type', 'object_id', 'my_order']


# Register polymorphic content types
admin.site.register(Text)
admin.site.register(Video)
admin.site.register(Image)
admin.site.register(File)
admin.site.register(Comment)





# admin.site.register(Subject)
# admin.site.register(Course)
# admin.site.register(Module)
# admin.site.register(Text)
# admin.site.register(Video)
# admin.site.register(Image)
# admin.site.register(File)
# admin.site.register(Topic)