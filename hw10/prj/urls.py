
from django.contrib import admin
from django.urls import path
from single_pages import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('index/', views.main_page, name='index'),
    path('strawberry/', views.strawberry_page, name='strawberry'), # 👈 이 name='strawberry'가 필수!
    path('about/', views.about_page, name='about'),
]
