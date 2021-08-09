from django.contrib import admin
from alerts import models


admin.site.register(models.Product)
admin.site.register(models.Price)
admin.site.register(models.ProductAlert)
admin.site.register(models.Update)
