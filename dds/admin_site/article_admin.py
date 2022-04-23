from django.contrib.admin import ModelAdmin


class ArticleAdmin(ModelAdmin):
    fields = ('type_operation', 'name',)
    list_display = ('name', 'type_operation',)
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('type_operation',)