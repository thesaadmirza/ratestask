from django.db import models
from django.conf import settings


# Commented because incoming parse sql structure not compatible with django

# class Region(models.Model):
#     # Regions Model
#     slug = models.SlugField(primary_key=True)
#     name = models.CharField(max_length=200)
#     parent_slug = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
#
#     class Meta:
#         db_table = 'regions'
#
#     def __str__(self):
#         return self.slug
#
#
# class Port(models.Model):
#     # Port Model
#     code = models.CharField(max_length=50, primary_key=True)
#     name = models.CharField(max_length=200)
#     parent_slug = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='ports')
#
#     class Meta:
#         db_table = 'ports'
#
#     def __str__(self):
#         return self.code
#
#
# class Price(models.Model):
#     orig_code = models.ForeignKey(Port, on_delete=models.CASCADE, related_name='origin')
#     dest_code = models.ForeignKey(Port, on_delete=models.CASCADE, related_name='destination')
#     day = models.DateField()
#     price = models.IntegerField()
#
#     class Meta:
#         db_table = 'prices'
#
#
#     def __str__(self):
#         str(self.day) + ' - ' + str(self.price)
