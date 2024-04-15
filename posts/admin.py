from django.contrib import admin

from posts.models import Posts, Category, Comment, Contact


class PostsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published_at', 'status']
    list_filter = ['status', 'created_at', 'published_at']
    date_hierarchy = 'published_at'
    search_fields = ['title', 'body', 'author']
    ordering = ['status', 'published_at']



admin.site.register(Posts, PostsAdmin)
admin.site.register(Category)
admin.site.register(Contact)




@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'body', 'created_time', 'active']
    list_filter = ['active', 'created_time']
    search_fields = ['user', 'body']
    actions = ['disable_comments', 'activate_comments']

    def disable_comments(self, request, queryset):
        queryset.update(active=False)

    def activate_comments(self, request, queryset):
        queryset.update(active=True)
