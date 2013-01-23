from app.models import *
import shutil
upload_path = "/srv/webapp/mysite/mysite/fratography_static/uploads/"
folder_path = "/srv/webapp/mysite/mysite/fratography_static/"

def copy_album(album_name, folder_name):
    album = Album.objects.get(name=album_name)
    for each_image in AlbumImage.objects.filter(album=album):
        shutil.copy(upload_path + each_image.image,
                    folder_path + folder_name)