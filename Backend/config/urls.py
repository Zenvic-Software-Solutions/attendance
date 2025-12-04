from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("common/", include("apps.BASE.urls")),
    path("access/", include("apps.ACCESS.urls")),
    path("cms/", include("apps.CMS.urls")),
    path('', TemplateView.as_view(template_name='index.html')),
    
    # re_path(r"^(?!media/|assets/).*", TemplateView.as_view(template_name="index.html")),
]

# Static & Media Files
# ------------------------------------------------------------------------------
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
