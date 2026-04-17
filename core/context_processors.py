from .models import SiteSettings


def site(request):
    try:
        settings = SiteSettings.load()
    except Exception:
        settings = None
    return {"site_settings": settings}
