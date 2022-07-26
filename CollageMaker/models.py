from django.db import models
from django.core.files.storage import FileSystemStorage
from urllib.request import urlopen
from tempfile import NamedTemporaryFile
from django.core.files import File
from django.conf.global_settings import MEDIA_URL
from KolazeZdjec.settings import MEDIA_ROOT


class Collage(models.Model):

    collage = models.ImageField(max_length=250, upload_to=f"{MEDIA_ROOT}/collages")
    # picture_1 = models.ImageField(upload_to=f'{MEDIA_URL}images/')
    # picture_2 = models.ImageField(upload_to=f'{MEDIA_URL}images/')
    # picture_3 = models.ImageField(upload_to=f'{MEDIA_URL}images/')
    # picture_4 = models.ImageField(upload_to=f'{MEDIA_URL}images/')
    # picture_5 = models.ImageField(upload_to=f'{MEDIA_URL}images/')
    # picture_6 = models.ImageField(upload_to=f'{MEDIA_URL}images/')


class Image_iItem(models.Model):
    image_file = models.ImageField(upload_to="images/")
    image_url = models.URLField()
