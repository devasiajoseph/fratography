from django.conf import settings
from app.models import AlbumCategory


def upload_path(context):
    return {"UPLOAD_PATH": settings.UPLOAD_PATH}

def categories(context):
    fraternities = AlbumCategory.objects.filter(
        parent=AlbumCategory.objects.get(name="Fraternity")
    )
    sororities = AlbumCategory.objects.filter(
        parent=AlbumCategory.objects.get(name="Sorority")
    )
    return {"fraternities": fraternities,
            "sororities": sororities}