
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API Routes
    path("posts/compose", views.compose, name="compose"),
    path("posts", views.show_posts, name="show_posts"),
    path("posts/<int:post_id>", views.post, name="post"),
    path("posts/<str:page>", views.page, name="page"),
]
