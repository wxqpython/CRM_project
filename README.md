# CRM_project知识点


## 一 CRM_project中结构化数据相关

情况一
```
v1=[11,22]
v2 = v1
v2.append(33)
print(v1)  # 结果[11,22,33]

说明： 
1 列表是可变数据类型。
2 append操作是引用数据，v2/v1会指向同一个内存地址
3 要想数据在传递过程中不改变，可切片传值v2=v1[0:2]
```

情况二

```
x = [
    {'name':'x1','child':[]},
    {'name':'x2','child':[]}
]

x[0]['child'].append(x[1])
x[1]['active'] = True

print(x)
[
	{'name': 'x1', 'child': [{'name': 'x2', 'child': [], 'active': True}]},
	 {'name': 'x2', 'child': [], 'active': True}
	]
```

情况 三：
```
l1 = [
    {"name":'wxq'},
    {"name":'pp'},
]

l2 = []
for item in l1:
    l2.append(item)  #append 会引用l1同一个内存地址
l2[0]['name'] = "xxx"
print(l1)            #append 会引用l1同一个内存地址,引起l1数值也改变
```

情况四
结合特性结构化数据一
```
comment_list=[
    {'nid':1,'content':111,'parent_id':None},
    {'nid':2,'content':222,'parent_id':None},
    {'nid':3,'content':333,'parent_id':None},
    {'nid':4,'content':444,'parent_id':1},
    {'nid':5,'content':555,'parent_id':4},
    {'nid':6,'content':666,'parent_id':1},
    {'nid':7,'content':777,'parent_id':2},
]
d={}  # 字典用于中转数据
for i in comment_list:
    i["child"] = []
    nid = i['nid']
    d[nid] =i
ret = []   # 最终我们要得到列表数据
for v in d.values():
    if v['parent_id']:
        parent_id = v['parent_id']
        d[parent_id]['child'].append(v)
    else:
        ret.append(v)

for i in ret:
    print(i)
```

```
 总结
# 总体思路; 先加"child":[],再把列表变为字典，再把字典变为列表
# 运用知识：append(可变数据类型)时会引用同一个内存地址
```

情况五
结合特性结构化数据二
```
import re
permission_menu_list = [
    {'id': 1, 'title': '用户列表', 'url': '/users/', 'pid': None, 'menu_id': 1, 'menu__name': '菜单1'},
    {'id': 2, 'title': '添加用户', 'url': '/users/add/', 'pid': 1, 'menu_id': 1, 'menu__name': '菜单1'},
    {'id': 3, 'title': '删除用户', 'url': '/users/del/(\d+)/', 'pid': 1, 'menu_id': 1,'menu__name': '菜单1'},
    {'id': 4, 'title': '修改用户', 'url': '/users/edit/(\d+)/', 'pid': 1, 'menu_id': 1,'menu__name': '菜单1'},
    {'id': 5, 'title': '主机列表', 'url': '/hosts/', 'pid': None, 'menu_id': 1, 'menu__name': '菜单1'},
    {'id': 6, 'title': '添加主机', 'url': '/hosts/add/', 'pid': 5, 'menu_id': 1, 'menu__name': '菜单1'},
    {'id': 7, 'title': '删除主机', 'url': '/hosts/del/(\d+)/', 'pid': 5, 'menu_id': 1,'menu__name': '菜单1'},
    {'id': 8, 'title': '修改主机', 'url': '/hosts/edit/(\d+)/', 'pid': 5, 'menu_id': 1,'menu__name': '菜单1'}
]


permission_menu_dict={}

for i in permission_menu_list:
    if not i['pid']:
        permission_menu_dict[i['id']] = i

for i in permission_menu_list:
    if i['pid']:
        permission_menu_dict[i['pid']]['active'] = True
    else:
        i['active'] = True

for k,v in permission_menu_dict.items():
    print(k,v)
```



情况六
结合特性结构化数据三
```
data_list = {
    5: {'id': 5, 'title': '主机列表', 'url': '/hosts/', 'pid': None, 'menu_id': 1, 'menu__name': '菜单1'},
    1: {'id': 1, 'title': '用户列表', 'url': '/users/', 'pid': None, 'menu_id': 1, 'menu__name': '菜单1', 'active': True},
    10: {'id': 10, 'title': 'xx列表', 'url': '/hosts/', 'pid': None, 'menu_id': 2, 'menu__name': '菜单2'}
}

result = {}
for item in data_list.values():
    id=item['id']
    title=item['title']
    url=item['url']
    menu_id = item['menu_id']
    menu_name = item['menu__name']
    active = item.get("active", False)
    temp = {'id':id , 'title': title, 'url':url,'active':active}
    if menu_id in result:
        result[menu_id]['child'].append(temp)
        if item.get("active", False):
            result[menu_id]["active"] =True
    else:
        result[menu_id] = {
            'menu_name':menu_name,
            'active':active,
            'child':[temp]
        }
for k,v in result.items():
    print(k,v)
```

## 二 CRM_project中rbac实现
```
rbac: 全称(Role base access control)，基于角色的权限控制.
实现逻辑或代码逻辑梳理
1 设计好表结构，写好models.py
2 用户登录，获取当前用户所有权限列表，对权限列表结构化后放入Session中
3 用户再次访问，获取用户请求的URL，与Session中的URL进行比较（基于中间件）
	获取当前请求的URL：request.path_info
        其中有request.permission_codes/re.match的补充
	
4 用户菜单如何显示？
	1，URL中有正则表过式的不能作为菜单显示
	2，菜单默认选中，
	3，二级菜单
	实现这个3点就要再定义下models class: Menu/再把权限+权限组+菜单列表直接写入Session用于菜单展示
	request.session[settings.PERMISSION_MENU_SESSION_KEY] = permission_memu_list
	
	当再次取出permission_memu_list时，需要经过2交结构化数据才能得到我们想要的结查，再把这个结果传给前端，前端经过2层for循环完成菜单展示
5 页面显示时，根据权限来控制页面是否显示指定按钮，权根的控制粒度：按钮级别

注意前端知识:
   1  static/templates优先在项目下找或说外层找，找不到才到各个app/static, app/templates下找，也就是说项目目录优先
   2  inclusion_tag 用法
   
```
#### inclusion_tag用法
```
templatetags/rbac.py定义
from django.template import Library
import re
from django.conf import settings
'''
{% menu_tag %}
'''
register = Library()

@register.inclusion_tag("rbac/tpl.html")
def menu_tag(request,):
    current_url  = request.path_info
    #获取Session中菜单信息，自动生成二级菜单，[默认选中，默认展开]
    permission_menu_list=request.session.get(settings.PERMISSION_MENU_SESSION_KEY)

    # 菜单信息处理一次
    per_dict = {}
    for item in permission_menu_list:
        if not item["pid"]:
            per_dict[item["id"]] = item

    for item in permission_menu_list:
        reg = settings.REX_FORMAT.format(item["url"])
        if not re.match(reg, current_url):
            continue
        if item["pid"]:
            per_dict[item["pid"]]["active"] = True
        else:
            item["active"] = True

    # print(per_dict)
    # 菜单信息处理二次
    menu_result = {}
    for item in per_dict.values():
        id = item['id']
        title = item['title']
        url = item['url']
        menu_id = item['menu_id']
        menu_name = item['menu__name']
        active = item.get("active", False)
        temp = {'id': id, 'title': title, 'url': url, 'active': active}
        if menu_id in menu_result:
            menu_result[menu_id]['child'].append(temp)
            if item.get("active", False):
                menu_result[menu_id]["active"] = True
        else:
            menu_result[menu_id] = {
                'menu_name': menu_name,
                'active': active,
                'child': [temp]
            }

    print(menu_result)
    return {"menu_result":menu_result}
```

```
rbac/tpl.html位于rbac/templates/rbac/tpl.html
{% for menu in  menu_result.values %}
    <div class="menu-item">
        <div class="menu-title">{{ menu.menu_name }}</div>
    {% if menu.active %}
        <div class="menu-content">
    {% else %}
        <div class="menu-content hide">
    {% endif %}

            {% for per in menu.child %}
                {% if per.active %}
                    <a href="{{ per.url }}" class="active">{{ per.title }}</a>
                {% else %}
                    <a href="{{ per.url }}">{{ per.title }}</a>
                {% endif %}

            {% endfor %}

        </div>
    </div>
{% endfor %}

```

```
运用
{% load rbac %}
...
{% menu_tag request %}
```


