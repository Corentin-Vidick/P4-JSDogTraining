from django.contrib import admin
from .models import Story, Thought
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Story)
class PostsAdmin(SummernoteModelAdmin):

    list_display = ('title', 'slug', 'status', 'created_on')
    search_fields = ['title', 'content']
    list_filter = ('status', 'created_on')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)


@admin.register(Thought)
class ThoughtsAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_thoughts']

    def approve_thoughts(self, request, queryset):
        queryset.update(approved=True)
