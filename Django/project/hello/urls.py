from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index") # when use this path, it will run index function
]