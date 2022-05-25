from django.urls import path
from . import views

urlpatterns = [
    # when use this path, it will run index function
    path("", views.index, name="index"), 
    path("world", views.world, name="world"),
    path("jean", views.jean, name="jean"),
    path("fuyang", views.fuyang, name="fuyang"),

    path("<str:name>", views.greet, name="greet")
]
    