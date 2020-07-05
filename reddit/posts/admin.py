from django.contrib import admin
from .models import Subreddit, Post, PostVotes, PostComment

# Register your models here.
class MyClassAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified', 'slug')

class MyChildren(admin.ModelAdmin):
    readonly_fields = ('children', )

admin.site.register(Subreddit, MyClassAdmin)
admin.site.register(Post, MyClassAdmin)
admin.site.register(PostVotes)
admin.site.register(PostComment, MyChildren)
