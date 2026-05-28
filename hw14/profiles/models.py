from django.core.exceptions import ValidationError
from django.db import models


class SiteProfile(models.Model):
    name_ko = models.CharField(max_length=80)
    name_en = models.CharField(max_length=80)
    tagline_ko = models.CharField(max_length=160)
    tagline_en = models.CharField(max_length=160)
    bio_ko = models.TextField()
    bio_en = models.TextField()
    location_ko = models.CharField(max_length=80, blank=True)
    location_en = models.CharField(max_length=80, blank=True)
    contact_email = models.EmailField(blank=True)
    hero_image = models.ImageField(upload_to="profile/", blank=True)
    hero_image_alt = models.CharField(max_length=160, blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "site profile"
        verbose_name_plural = "site profile"

    def __str__(self):
        return self.name_ko

    def clean(self):
        if not self.pk and SiteProfile.objects.exists():
            raise ValidationError("Only one site profile can be created.")

    def name_for(self, language):
        return self.name_en if language == "en" else self.name_ko

    def tagline_for(self, language):
        return self.tagline_en if language == "en" else self.tagline_ko

    def bio_for(self, language):
        return self.bio_en if language == "en" else self.bio_ko

    def location_for(self, language):
        return self.location_en if language == "en" else self.location_ko
