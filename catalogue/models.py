from django.db import models

# Create your models here.
 from oscar.apps.catalogue.abstract_models import AbstructProduct

 class Product( AbstructProduct ): 
   video_url = models.URLField()

   from osccar.apps.catalogue.models import *

