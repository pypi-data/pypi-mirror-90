# coding=gbk
from abc import ABCMeta, abstractmethod

"""
�洢��
"""


class BaseStorage(metaclass=ABCMeta):
    @abstractmethod
    def set(self, key, value, **kwargs):
        """
        �洢key-value����
        :param key: �洢��key
        :param value: �洢��key��Ӧ��ֵ
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


class SimpleStorage(BaseStorage):
    def __init__(self):
        self._hash_storage = dict()

    def set(self, key, value, **kwargs):
        self._hash_storage[key] = value

    def get(self, key):
        return self._hash_storage.get(key, None)

    def delete(self, key):
        value = self._hash_storage.get(key, None)
        del self._hash_storage[key]
        return value
