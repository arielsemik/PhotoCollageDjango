from django.db import models

from KolazeZdjec.settings import MEDIA_ROOT


class Collage(models.Model):

    collage = models.ImageField(max_length=250, upload_to=f"{MEDIA_ROOT}/collages/")



class Image_iItem(models.Model):
    image_file = models.ImageField(upload_to="images/")
    image_url = models.URLField()
