from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("wiki/<str:title>/edit", views.entry_edit, name="entry_edit"),
    path("create/", views.create, name="create"),
    path("wiki/", views.random_page, name="random_page"),
]
