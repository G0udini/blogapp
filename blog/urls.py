from django.contrib import admin
from django.urls import path, include
import debug_toolbar


urlpatterns = [
    path("blog/", include("blog_app.urls", namespace="blog")),
    path("admin/", admin.site.urls),
    path("__debug__/", include(debug_toolbar.urls)),
]
