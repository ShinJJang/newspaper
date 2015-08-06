from django.contrib import admin
from news.models import Thread, Vote, Comment

admin.site.register(Thread)
admin.site.register(Vote)
admin.site.register(Comment)

