#!/usr/bin/python
# coding:utf-8

import os
import sys

try:
    reload(sys)
    sys.setdefaultencoding("utf8")
except:
    pass

import os
import sys

cur_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append("%s/" % cur_dir)

from setuptools import setup
from setuptools import find_packages

setup(
    name="SimpleVue",
    version="20210106.6",
    keywords=("vue", "python", "pyvue", "simplevue"),
    description="SimpleVue",
    long_description="vue构建前端，并使用python进行组件化",
    license="MIT License",

    url="https://gitee.com/lijiacai/SimpleVue.git",
    author="Lijiacai",
    author_email="1050518702@qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[],  # 这个项目需要的第三方库
    scripts=[]
)
