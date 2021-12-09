from blog_app.feeds import LatestPostsFeed
from django.urls import path
from .views import post_detail, post_list, post_share, post_search
from .feeds import LatestPostsFeed

app_name = "blog_app"
urlpatterns = [
    path("search/", post_search, name="post_search"),
    path("feed/", LatestPostsFeed(), name="post_feed"),
    path("tag/<slug:tag_slug>", post_list, name="post_list_by_tag"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/", post_detail, name="post_detail"
    ),
    path("<int:post_id>/share/", post_share, name="post_share"),
    path("", post_list, name="post_list"),
]
