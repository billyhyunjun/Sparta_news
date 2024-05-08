from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    path("", views.ArticleAPIView.as_view(), name="article"),
    path("detail/<int:article_id>/", views.ArticleDetailAPIView.as_view(), name="detail"),
    path("like/<int:article_id>/", views.like, name="like"),
    path("favorite/<int:article_id>/", views.favorite, name="favorite"),
    path("comment/<int:comment_id>/", views.CommentAPIView.as_view(), name="comment"),
]
