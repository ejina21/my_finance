from django.contrib import admin

from dds.admin_site.article_admin import ArticleAdmin
from dds.admin_site.operation_admin import OperationAdmin
from dds.admin_site.user_admin import CustomUserAdmin
from dds.models import CustomUser, Article, Operation

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Operation, OperationAdmin)
admin.site.register(Article, ArticleAdmin)
