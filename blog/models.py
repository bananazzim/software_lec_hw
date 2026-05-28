from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone


class PublishedQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status=Post.Status.PUBLISHED, published_at__lte=timezone.now())


class Category(models.Model):
    title_ko = models.CharField("Korean title", max_length=80)
    title_en = models.CharField("English title", max_length=80)
    slug = models.SlugField(unique=True)
    description_ko = models.CharField(max_length=180, blank=True)
    description_en = models.CharField(max_length=180, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "title_ko"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title_ko

    def title_for(self, language):
        return self.title_en if language == Post.Language.EN else self.title_ko

    def description_for(self, language):
        return self.description_en if language == Post.Language.EN else self.description_ko


class Tag(models.Model):
    name = models.CharField(max_length=48, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Post(models.Model):
    class Language(models.TextChoices):
        KO = "ko", "Korean"
        EN = "en", "English"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    language = models.CharField(max_length=2, choices=Language.choices, default=Language.KO)
    title = models.CharField(max_length=160)
    slug = models.SlugField()
    summary = models.TextField(max_length=420)
    body = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")
    translation = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="translated_versions",
    )
    featured_image = models.ImageField(upload_to="posts/", blank=True)
    image_alt = models.CharField(max_length=160, blank=True)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.DRAFT)
    is_featured = models.BooleanField(default=False)
    reading_minutes = models.PositiveSmallIntegerField(default=1)
    published_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PublishedQuerySet.as_manager()

    class Meta:
        ordering = ["-published_at", "-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["language", "slug"], name="unique_post_slug_per_language"),
            models.CheckConstraint(
                condition=~Q(translation=models.F("id")),
                name="post_translation_cannot_point_to_self",
            ),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        words = len(self.body.split())
        self.reading_minutes = max(1, round(words / 220))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        if self.language == self.Language.EN:
            return reverse("post_detail_en", kwargs={"slug": self.slug})
        return reverse("post_detail", kwargs={"slug": self.slug})

    @property
    def public_translation(self):
        if self.translation and self.translation.is_public:
            return self.translation
        return self.translated_versions.published().first()

    @property
    def is_public(self):
        return self.status == self.Status.PUBLISHED and self.published_at <= timezone.now()
