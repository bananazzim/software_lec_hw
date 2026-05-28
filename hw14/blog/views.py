from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from profiles.models import SiteProfile

from .models import Category, Post


def _published_posts(language):
    return (
        Post.objects.published()
        .filter(language=language)
        .select_related("category", "translation")
        .prefetch_related("tags")
    )


def _language_context(language, active="home", switch_url=None):
    other_language = "en" if language == "ko" else "ko"
    return {
        "language": language,
        "other_language": other_language,
        "active_nav": active,
        "language_switch_url": switch_url or reverse("home_en" if other_language == "en" else "home"),
    }


def home(request, language="ko"):
    posts = _published_posts(language)
    featured_post = posts.filter(is_featured=True).first() or posts.first()
    latest_posts = posts.exclude(pk=getattr(featured_post, "pk", None))[:6]
    categories = Category.objects.filter(posts__status=Post.Status.PUBLISHED, posts__language=language).distinct()
    context = {
        **_language_context(language, active="home"),
        "profile": SiteProfile.objects.first(),
        "featured_post": featured_post,
        "latest_posts": latest_posts,
        "categories": categories,
    }
    return render(request, "blog/home.html", context)


def post_list(request, language="ko"):
    posts = _published_posts(language)
    categories = Category.objects.filter(posts__status=Post.Status.PUBLISHED, posts__language=language).distinct()
    context = {
        **_language_context(language, active="essays"),
        "posts": posts,
        "categories": categories,
        "heading": "Essays" if language == "en" else "에세이",
    }
    return render(request, "blog/post_list.html", context)


def category_detail(request, slug, language="ko"):
    category = get_object_or_404(Category, slug=slug)
    posts = _published_posts(language).filter(category=category)
    context = {
        **_language_context(language, active="essays"),
        "posts": posts,
        "category": category,
        "heading": category.title_for(language),
    }
    return render(request, "blog/post_list.html", context)


def post_detail(request, slug, language="ko"):
    post = get_object_or_404(_published_posts(language), slug=slug)
    related_posts = (
        _published_posts(language)
        .filter(Q(category=post.category) | Q(tags__in=post.tags.all()))
        .exclude(pk=post.pk)
        .distinct()[:3]
    )
    translation = post.public_translation
    switch_url = translation.get_absolute_url() if translation else reverse("home_en" if language == "ko" else "home")
    context = {
        **_language_context(language, active="essays", switch_url=switch_url),
        "post": post,
        "related_posts": related_posts,
        "translation": translation,
    }
    return render(request, "blog/post_detail.html", context)


def about(request, language="ko"):
    context = {
        **_language_context(language, active="about"),
        "profile": SiteProfile.objects.first(),
    }
    return render(request, "profiles/about.html", context)


def search(request, language="ko"):
    query = request.GET.get("q", "").strip()
    posts = _published_posts(language)
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(summary__icontains=query) | Q(body__icontains=query))
    else:
        posts = posts.none()
    context = {
        **_language_context(language, active="search"),
        "query": query,
        "posts": posts,
    }
    return render(request, "blog/search.html", context)
