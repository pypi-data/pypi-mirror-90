from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requires = [
      "redis>=3.5.3"
]

setup(name='csy-memory-cache',
      version='0.1.4',
      description='python memory cache base python3',
      url='https://github.com/1278651995/python-memory-cache',
      author='chensy-jp',
      author_email='1278651995@qq.com',
      license='Apache-2.0',
      packages=['memory_cache', 'memory_cache.extend.apis', 'memory_cache.extend.storages'],
      zip_safe=False,
      python_requires='>=3.6'
)

