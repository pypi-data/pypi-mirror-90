# python-memory-cache

#### 介绍

python实现内存的缓存器，用于小数据存储。

默认使用LRU作为回收算法。

#### 安装
```shell script
pip install csy-memory-cache
```

#### 结构图

![结构图](./docs/结构图.png)



#### 使用教程

实例化

```python
from memory_cache.api import SimpleCacheAPI

api = SimpleCacheAPI()
# or
from memory_cache.algorithms import LRU
from memory_cache.storage import SimpleStorage

api = SimpleCacheAPI(algorithms=LRU, storage=SimpleStorage, max_size=1024)
```

存储

```python
api.set(key, value)
# or 
api.set(key, value, expire=10)  # 单位秒(s)
```

获取

```python
api.get(key)
```

删除

```python
api.delete(key)
```



#### 扩展

该缓存器中所有组件均可扩展，其中API扩展只需满足```BaseCacheAPI```定义、存储扩展只需满足```BaseStorage```定义， 回收算法只需满足```BaseAlgorithms```定义


#### 更新记录


- 20210108

1. 增加api中的功能：```exists(key)```， 用以判断是否key存在

2. 增加api中的功能：```clear()```， 清空键

3. 增加api的命名空间存储方式，如```nset(name, key, value)```， 存储在命名空间name下的key-value

4. 增加基于redis的扩展API和存储，使用方法：

   ```python
   from memory_cache.extend.apis.redis_api import RedisAPI
   from memory_cache.extend.storages.redis_storage import RedisStorage
   
   
   redis_api = RedisAPI(
       RedisStorage("10.10.10.112", port=6379, db=1, password="goodsang123")
   )
   ```

   