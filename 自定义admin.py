

request.GET 数据类型为QueryDict 本身不可修改，必须修改属性才能被修改_mutable = True
      
request.GET._mutable = True

# 运用
import copy
params = request.GET()
params._mutable = True
params["page"] = 2      # QueryDict()
params.urlencode()      # 转为了page=1&key=xx



      
      
      
   
   


