from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("en/", views.home, {"language": "en"}, name="home_en"),
    path("essays/", views.post_list, name="post_list"),
    path("en/essays/", views.post_list, {"language": "en"}, name="post_list_en"),
    path("topics/<slug:slug>/", views.category_detail, name="category_detail"),
    path("en/topics/<slug:slug>/", views.category_detail, {"language": "en"}, name="category_detail_en"),
    path("essays/<slug:slug>/", views.post_detail, name="post_detail"),
    path("en/essays/<slug:slug>/", views.post_detail, {"language": "en"}, name="post_detail_en"),
    path("about/", views.about, name="about"),
    path("en/about/", views.about, {"language": "en"}, name="about_en"),
    path("search/", views.search, name="search"),
    path("en/search/", views.search, {"language": "en"}, name="search_en"),
]
