# 自定义Django admin 
http://www.cnblogs.com/wupeiqi/articles/7444717.html    # 自定义Django admin参考博客
  




一  Django admin工作流程：
1 注册models_class，生成URL
    admin.py注册models_class如models.UserInfo
      from django.template import admin
      from app01 import models
      admin.site.registry(models.UserInfo)
   生成4个URL分别是如下：
   app01/userinfo/
   app01/userinfo/add/
   app01/userinfo/1/change/
   app01/userinfo/1/delete/
   
2 


#URL include原理
partterns = [
   url(r'^admin', admin.site.urls),            # admin.site.urls 返回形如（[],None,None）的元组.
   url(r'^backend', include('backend.urls')),  # include 同样返回形如（[],None,None）的元组.
   # 也可以写成形如 include([],None,None) 格式.
 ]



二  制作arya启动文件
    1  创建一个arya 的app
    2  settings.py 注册app
        -  'arya.apps.AryaConfig',
    3  在arya apps.py文件定义ready方法
      class AryaConfig(AppConfig):
       name = 'arya'

       def ready(self):
           from django.utils.module_loading import autodiscover_modules
           autodiscover_modules("xxx")

    4 启动项目时会先在执行所有app下的xxx.py文件，当然前提是这些app也是settings.py注册好的
   
   
   三 单例模式
   
      单例模式有很多种实现方式：
      其中一种：利用模块多次导入时，除第一次外不会真正执行模块代码。
                  如果模块中有实例化对象操作，那么多次导入也不会真正实例化多个对象，而是同一个实例
                  如果在一个程序先运行的文件改变了实例数据或属性，后运行的文件导入后读这个实例就会有数据或属性
            
     示例：
     随便定义一个实例化对象的文件arya/service.v1
      class AryaSite():
          def __init__(self):
              self._registry = {}

          def register(self,class_name,config_class):
              self._registry[class_name] = config_class

         site = AryaSite()
            
     在我们定义的启动文件app01/xxx.py中写入代码(因为会先执行xxx.py)
      from arya.service import v1
      v1.site.register("k1","v1")
      v1.site.register("k2","v2")
      v1.site.name = 'wxq'
      
      项目urls.py中写入
      from arya.service import v1
      print(v1.site._registry)
      print(v1.site.name)
      
      启动项目时，先执行app01/xxx.py,后执行urls.py文件，程序读到了实例的数据并不是重新实例化新对象，这就是单例模式的运用
      
      
      
   
   


