from django.conf import settings
from app.models import AlbumCategory


def upload_path(context):
    return {"UPLOAD_PATH": settings.UPLOAD_PATH}

def categories(context):
    fraternities = AlbumCategory.objects.filter(
        parent=AlbumCategory.objects.get(name="Fraternity")
    ).order_by('name')
    sororities = AlbumCategory.objects.filter(
        parent=AlbumCategory.objects.get(name="Sorority")
    ).order_by('name')
    return {"fraternities": fraternities,
            "sororities": sororities}