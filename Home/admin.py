from django.contrib import admin
from .models import Topic, Comment


admin.site.register(Comment)

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at")
    readonly_fields = ("created_at",)