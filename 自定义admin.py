from django.template import admin
from app01 import models


admin.site.registry(models.UserInfo)

