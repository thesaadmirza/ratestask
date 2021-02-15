from django.db import models
from django.conf import settings


class Region(models.Model):
    # Regions Model
    slug = models.SlugField(primary_key=True)
    name = models.CharField(max_length=200)
    parent_slug = models.ForeignKey('self', on_delete=models.CASCADE)

    class Meta:
        db_table = 'regions'

    def __str__(self):
        return self.slug


class Port(models.Model):
    # Port Model
    code = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=200)
    parent_slug = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='ports')

    class Meta:
        db_table = 'ports'

    def __str__(self):
        return self.code


class Price(models.Model):
    orig_code = models.ForeignKey(Port, on_delete=models.CASCADE, related_name='origin')
    dest_code = models.ForeignKey(Port, on_delete=models.CASCADE, related_name='destination')
    day = models.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    price = models.IntegerField()

    def __str__(self):
        self.orig_code.code + ' - ' + self.dest_code.code
