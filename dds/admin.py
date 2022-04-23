from django.contrib import admin

from dds.models import CustomUser, Article, Operation

admin.site.register(CustomUser)
admin.site.register(Operation)
admin.site.register(Article)
