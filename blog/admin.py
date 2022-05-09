from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms


class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = "__all__"


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class PostAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    save_on_top = True
    prepopulated_fields = {"slug": ("title", )}
    list_display = ["id", 'title', 'slug', 'category', 'created_at', 'get_photo']
    list_display_links = ['title']
    search_fields = ("title", )
    list_filter = ("category", 'tags')
    readonly_fields = ("views", 'created_at', 'get_photo')
    fields = ['title', 'slug', 'category', 'tags', 'content', 'photo', 'get_photo', 'views', 'created_at']

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        return '-'

    get_photo.short_description = "Миниатюра"


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
