#!/usr/bin/env python
from setuptools import setup


setup(
    name='rest_framework_pagination',
    version='0.0.1',
    license='MIT',
    url='https://github.com/imzaur/drf_multi_queryset_pagination',
    description='Django REST framework limit/offset pagination with multiple queryset support',
    long_description=open('README.rst', 'r', encoding='utf-8').read(),
    author='Zaur Magamednebiev',
    author_email='imzaur777@gmail.com',
    install_requires=[
        'django',
        'djangorestframework'
    ],
    python_requires='>=3.6',
    packages=['rest_framework_pagination']
)
