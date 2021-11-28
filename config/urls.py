from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from config import settings

handler404 = 'config.views.custom_page_not_found'
handler500 = 'config.views.custom_server_error'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('blog/', include('blog.urls')),
    path('captcha/', include('captcha.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('', include('serials.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
