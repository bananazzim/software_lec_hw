from django.urls import path
from . import views

urlpatterns = [
    path("", views.ListListView.as_view(), name="index"),
    path("list/<int:list_id>/", views.ItemListView.as_view(), name="list"),
    path("list/new/", views.ListCreate.as_view(), name="list-add"),
    path("list/<int:pk>/update/", views.ListUpdate.as_view(), name="list-update"),
    path("list/<int:list_id>/item/new/", views.ItemCreate.as_view(), name="item-add"),
    path("item/<int:pk>/update/", views.ItemUpdate.as_view(), name="item-update"),
    path("item/<int:pk>/delete/", views.ItemDelete.as_view(), name="item-delete"),
]