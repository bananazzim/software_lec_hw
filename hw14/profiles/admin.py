from django.contrib import admin

from .models import SiteProfile


@admin.register(SiteProfile)
class SiteProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Identity", {"fields": ("name_ko", "name_en", "tagline_ko", "tagline_en")}),
        ("Biography", {"fields": ("bio_ko", "bio_en", "location_ko", "location_en")}),
        ("Media", {"fields": ("hero_image", "hero_image_alt")}),
        ("Links", {"fields": ("contact_email", "github_url", "linkedin_url", "instagram_url")}),
    )
    readonly_fields = ("created_at", "updated_at")
