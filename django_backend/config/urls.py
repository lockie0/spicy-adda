from django.urls import include, path

from .views import frontend_asset, frontend_index, legacy_asset

urlpatterns = [
    path('api/', include('catalog.urls')),
    path('assets/<path:path>', frontend_asset, name='frontend-asset'),
    path('legacy/static/<path:path>', legacy_asset, name='legacy-asset'),
    path('', frontend_index, name='frontend-index'),
]
