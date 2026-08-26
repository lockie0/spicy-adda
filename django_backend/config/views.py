from django.conf import settings
from django.http import FileResponse, Http404


FRONTEND_DIST = settings.PROJECT_DIR / 'frontend' / 'dist'


def frontend_index(request):
    index_file = FRONTEND_DIST / 'index.html'
    if not index_file.exists():
        raise Http404('React frontend has not been built yet.')
    return FileResponse(index_file.open('rb'), content_type='text/html')


def frontend_asset(request, path):
    asset_root = FRONTEND_DIST / 'assets'
    asset_file = asset_root / path
    if not asset_file.is_file() or asset_root.resolve() not in asset_file.resolve().parents:
        raise Http404('Frontend asset not found.')
    return FileResponse(asset_file.open('rb'))


def legacy_asset(request, path):
    asset_file = settings.PROJECT_DIR / 'app' / 'static' / path
    if not asset_file.is_file() or settings.PROJECT_DIR not in asset_file.resolve().parents:
        raise Http404('Legacy asset not found.')
    return FileResponse(asset_file.open('rb'))
