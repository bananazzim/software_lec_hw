from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Category, Post, Tag


class BlogModelTests(TestCase):
    def test_published_manager_only_returns_public_posts(self):
        Post.objects.create(
            language=Post.Language.KO,
            title="Public",
            slug="public",
            summary="Visible summary",
            body="Visible body",
            status=Post.Status.PUBLISHED,
            published_at=timezone.now(),
        )
        Post.objects.create(
            language=Post.Language.KO,
            title="Draft",
            slug="draft",
            summary="Hidden summary",
            body="Hidden body",
            status=Post.Status.DRAFT,
            published_at=timezone.now(),
        )

        self.assertEqual(Post.objects.published().count(), 1)
        self.assertEqual(Post.objects.published().first().slug, "public")

    def test_translation_link_can_connect_bilingual_posts(self):
        ko = Post.objects.create(
            language=Post.Language.KO,
            title="첫 글",
            slug="note",
            summary="요약",
            body="본문",
            status=Post.Status.PUBLISHED,
            published_at=timezone.now(),
        )
        en = Post.objects.create(
            language=Post.Language.EN,
            title="First note",
            slug="note",
            summary="Summary",
            body="Body",
            status=Post.Status.PUBLISHED,
            published_at=timezone.now(),
            translation=ko,
        )

        self.assertEqual(en.public_translation, ko)


class BlogViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title_ko="일", title_en="Work", slug="work")
        self.tag = Tag.objects.create(name="writing", slug="writing")
        self.post = Post.objects.create(
            language=Post.Language.KO,
            title="공개 글",
            slug="public-note",
            summary="공개 요약",
            body="공개 본문",
            category=self.category,
            status=Post.Status.PUBLISHED,
            published_at=timezone.now(),
        )
        self.post.tags.add(self.tag)
        self.draft = Post.objects.create(
            language=Post.Language.KO,
            title="비공개 글",
            slug="draft-note",
            summary="비공개 요약",
            body="비공개 본문",
            status=Post.Status.DRAFT,
            published_at=timezone.now(),
        )

    def test_home_renders_public_post(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, "공개 글")
        self.assertNotContains(response, "비공개 글")

    def test_post_list_renders(self):
        response = self.client.get(reverse("post_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "공개 글")

    def test_post_detail_blocks_draft(self):
        response = self.client.get(reverse("post_detail", kwargs={"slug": self.draft.slug}))

        self.assertEqual(response.status_code, 404)

    def test_search_finds_public_post(self):
        response = self.client.get(reverse("search"), {"q": "공개"})

        self.assertContains(response, "공개 글")
        self.assertNotContains(response, "비공개 글")

    def test_about_page_renders_without_profile(self):
        response = self.client.get(reverse("about"))

        self.assertEqual(response.status_code, 200)

# Create your tests here.
