from django.contrib import admin
from django.urls import path, include
import debug_toolbar
from django.contrib.sitemaps.views import sitemap
from blog_app.sitemaps import PostSitemap
from django.conf import settings
from django.conf.urls.static import static

sitemaps = {
    "posts": PostSitemap,
}

urlpatterns = [
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("admin/", admin.site.urls),
    path("__debug__/", include(debug_toolbar.urls)),
    path("", include("blog_app.urls", namespace="blog")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
