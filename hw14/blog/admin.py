from django.contrib import admin
from django.utils.text import slugify

from .models import Category, Post, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title_ko", "title_en", "slug", "order")
    prepopulated_fields = {"slug": ("title_en",)}
    search_fields = ("title_ko", "title_en", "description_ko", "description_en")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "language", "status", "category", "is_featured", "published_at")
    list_filter = ("language", "status", "category", "tags", "is_featured")
    search_fields = ("title", "summary", "body")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("category", "tags", "translation")
    filter_horizontal = ("tags",)
    date_hierarchy = "published_at"
    fieldsets = (
        ("Publication", {"fields": ("language", "status", "is_featured", "published_at")}),
        ("Content", {"fields": ("title", "slug", "summary", "body")}),
        ("Organization", {"fields": ("category", "tags", "translation")}),
        ("Media", {"fields": ("featured_image", "image_alt")}),
    )

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = slugify(obj.title)
        super().save_model(request, obj, form, change)
