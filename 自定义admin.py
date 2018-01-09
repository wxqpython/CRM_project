# 自定义Django admin 

from django.template import admin
from app01 import models
admin.site.registry(models.UserInfo)

# include
partterns = [
   url(r'^admin', admin.site.urls),            # admin.site.urls 返回形如（[],None,None）的元组.
   url(r'^backend', include('backend.urls')),  # include 同样返回形如（[],None,None）的元组.
   # 也可以写成形如 include([],None,None) 格式.
 ]








