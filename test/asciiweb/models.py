from django.db import models


class RawImage(models.Model):
    """class to store all the images"""
    image = models.ImageField(upload_to="amg/")

    class Meta:
        verbose_name = "RawImage"
        verbose_name_plural = "RawImages"
        ordering = ("-pk",)

    def __str__(self):
        return self.image.url

    @property
    def get_image(self):
        """this method returns the url of the image"""
        return self.image.url
