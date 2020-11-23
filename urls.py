from django.urls import path

from . import views

app_name="encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("search",views.get_search, name="search"),
    path("Create",views.newPage, name="newPage"),
    path("random", views.randomPage, name="random"),
    path("edit<str:name>", views.editPage, name="editPage"),
    path("<str:name>", views.query, name="query"),
]
