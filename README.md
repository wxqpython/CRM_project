# CRM_project中结构化数据相关


## 数据类型学习笔记

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
    temp = {'id':id , 'title': title, 'url':url,'active':item.get("active",False)}
    if menu_id in result:
        result[menu_id]['child'].append(temp)
        if item.get("active",False):
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
