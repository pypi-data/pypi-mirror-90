# coding=gbk
import sys
from abc import ABCMeta, abstractmethod

from memory_cache.algorithms import LRU
from memory_cache.storage import SimpleStorage

"""
������API
"""


class BaseCacheAPI(metaclass=ABCMeta):
    @abstractmethod
    def set(self, key, value, expire=-1):
        """
        �洢key-value����
        :param key: �洢��key
        :param value: �洢��key��Ӧ��ֵ
        :param expire: �洢��ʱʱ�䣬Ĭ���ǲ������
        """
        pass

    @abstractmethod
    def get(self, key):
        """
        ����keyȡֵ
        :param key: �洢�ļ�
        :return: value: ��ȡ��ֵ
        """
        pass

    @abstractmethod
    def delete(self, key):
        """
        ɾ���洢�ļ�ֵ��
        :param key: ��
        :return: items: �洢�ļ���ֵ
        """
        pass

    @abstractmethod
    def exists(self, key):
        """
        �жϴ洢�ļ��Ƿ����
        :param key: ��
        :return: bool
        """
        pass

    @abstractmethod
    def clear(self):
        """
        ��ռ�
        """
        pass

    @abstractmethod
    def nset(self, name, key, value, expire=-1):
        pass

    @abstractmethod
    def nget(self, name, key):
        pass

    @abstractmethod
    def ndelete(self, name, key):
        pass

    @abstractmethod
    def nexists(self, name, key):
        pass


class SimpleCacheAPI(BaseCacheAPI):
    def __init__(self, storage=None, algorithms=None, max_size=1024, memory_limit=True):
        """
        :param storage: �洢�࣬[storage.BaseStorage]
        :param max_size: Ĭ�ϴ洢����ڴ�Ϊ1024�ֽڵ�����
        """
        self._storage = storage if storage is not None else SimpleStorage()
        self._alg = algorithms if algorithms is not None else LRU(self._storage)
        self.max_size = max_size
        self.memory_limit = memory_limit

    def exists(self, key):
        return key in self._alg.cache.keys()

    def clear(self):
        self._alg.clear()

    def set(self, key, value, expire=-1):
        if self.memory_limit:
            if sys.getsizeof(value) > self.max_size:
                assert ValueError('�����ڴ�����')
        return self._alg.set(key, value, expire)

    def get(self, key):
        return self._alg.get(key)

    def delete(self, key):
        return self._alg.delete(key)

    def nset(self, name, key, value, expire=-1):
        key_prefix = name
        return self.set(key_prefix + key, value, expire)

    def nget(self, name, key):
        key_prefix = name
        return self.get(key_prefix+key)

    def ndelete(self, name, key):
        key_prefix = name
        return self.delete(key_prefix + key)

    def nexists(self, name, key):
        key_prefix = name
        return self.exists(key_prefix + key)
