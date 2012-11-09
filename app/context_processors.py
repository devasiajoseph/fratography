from django.conf import settings


def upload_path(context):
    return {"UPLOAD_PATH": settings.UPLOAD_PATH}
