from django.urls import path
from . import views

# To prevent name collision with other application, we can specify the application name
app_name = "tasks"
urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add")
]