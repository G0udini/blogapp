from blog_app.feeds import LatestPostsFeed
from django.urls import path
from .views import PostShare, PostListView, PostDeatail, PostAdd
from .feeds import LatestPostsFeed

app_name = "blog_app"
urlpatterns = [
    path("feed/", LatestPostsFeed(), name="post_feed"),
    path("tag/<slug:tag_slug>/", PostListView.as_view(), name="post_list_by_tag"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/",
        PostDeatail.as_view(),
        name="post_detail",
    ),
    path("<int:post_id>/share/", PostShare.as_view(), name="post_share"),
    path("create/", PostAdd.as_view(), name="post_create"),
    path("", PostListView.as_view(), name="post_list"),
]
