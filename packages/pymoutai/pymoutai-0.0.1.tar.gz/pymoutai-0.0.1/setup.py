# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='pymoutai',
    version='0.0.1',
    description='JD Moutai Assistant',
    author='刘强东',
    url='https://item.jd.com/100012043978.html',
    author_email='liuqiangdong@jd.com',
    packages=find_packages(),
    install_requires=[  # 依赖列表
        'certifi == 2020.4.5.1',
        'chardet == 3.0.4',
        'idna == 2.9',
        'lxml == 4.5.1',
        'requests == 2.23.0',
        'urllib3 == 1.25.9'
    ],
    include_package_data=False,
    zip_safe=True,
)
