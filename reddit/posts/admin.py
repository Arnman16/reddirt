from django.contrib import admin
from .models import Subreddit, Post, PostVotes

# Register your models here.
class MyClassAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified', 'slug')

admin.site.register(Subreddit, MyClassAdmin)
admin.site.register(Post, MyClassAdmin)
admin.site.register(PostVotes)
