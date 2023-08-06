# Rainbond Python

Rainbond python cloud native development base library.

## Instructions

### DBConnect

```python
from rainbond_python.db_connect import DBConnect
db = DBConnect(db='db_name', collection='collection_name')
```

#### Write a docu

```python
insert_dict = {'name': 'Xiao Ming', 'age': 23}
if db.write_one_docu(docu=insert_dict):
    print('Insert success')
else:
    print('Insert failure')
```

#### Does docu exist

```python
examine_dict = {'name': 'Xiao Ming'}
if db.does_it_exist(docu=examine_dict):
    print('Docu already exists')
else:
    print('Docu does not exist')
```

#### Update docu

##### Modify the first

```python
find_dict = {'name': 'Xiao Ming'}
modify_dict = {'name': 'Xiao Hong'}
if db.update_docu(find_docu=find_dict, modify_docu=modify_dict):
    print('Update success')
else:
    print('Update failure')
```

##### Modify all

```python
find_dict = {'age': 23}
modify_dict = {'name': '23 year old'}
if db.update_docu(find_docu=find_dict, modify_docu=modify_dict, many=True):
    print('Update all success')
else:
    print('Update all failure')
```

## Reference

- [Restful API](https://www.runoob.com/w3cnote/restful-architecture.html) : Representational State Transfer
- [12 Factor](https://12factor.net/zh_cn/) : The twelve-factor app is a methodology for building software-as-a-service apps
- [RainBond](https://www.rainbond.com/docs/) : Cloud native and easy-to-use application management platform
