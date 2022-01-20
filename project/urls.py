from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.generic import RedirectView
from django.conf.urls.static import static

from project.router import router

admin.site.site_header = getattr(settings, 'PROJECT_NAME_HEADER')
admin.site.site_title = getattr(settings, 'PROJECT_NAME_TITLE')

urlpatterns = [
    path(
        '',
        RedirectView.as_view(
            url=f'{settings.FORCE_SCRIPT_NAME}/admin/' if settings.FORCE_SCRIPT_NAME else '/admin/'
        )
    ),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.ACTIVAR_HERRAMIENTAS_DEBUGGING:
    import debug_toolbar
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
