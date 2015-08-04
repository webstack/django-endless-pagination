# -*- coding: utf-8 -*-
#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

__version__ = '2.0.2'

PACKAGE_NAME = 'endless_pagination'

data_files = [
    "locale/*/LC_MESSAGES/*",
    "static/endless_pagination/js/*"
]

setup(
    name='webstack-django-endless-pagination',
    version=__version__,
    description=u"""Django Endless Pagination can be used to provide
    Twitter-style or Digg-style pagination""",
    long_description=open('README.rst').read(),
    author='Francesco Banconi',
    author_email='francesco.banconi@gmail.com',
    url='http://github.com/webstack/django-endless-pagination',
    keywords='django pagination ajax',
    packages=[
        PACKAGE_NAME,
        PACKAGE_NAME + '.templatetags'
    ],
    package_dir={
        PACKAGE_NAME: PACKAGE_NAME
    },
    package_data={
        PACKAGE_NAME: data_files
    },
    include_package_data=True,
    zip_safe=False,
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
)
