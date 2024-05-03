from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    path("", views.ArticleAPIView.as_view(), name="article"),
    path("detail/<int:article_id>/", views.ArticleDetailAPIView.as_view(), name="detail"),
    path("comment/<int:article_id>/", views.CommentAPIView.as_view(), name="comment"),
]
