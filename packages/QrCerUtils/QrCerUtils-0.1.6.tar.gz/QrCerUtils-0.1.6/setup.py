# -*- coding: utf-8 -*-
# @Time    : 2020/10/30 18:50
# @Author  : Dong Qirui
# @Software: PyCharm

from setuptools import setup, find_packages, Extension
from distutils.core import setup, Extension

import setuptools

with open( 'ReadMe.md', 'r' ) as fh :
    long_description = fh.read()

setuptools.setup(
        # 名称
        name='QrCerUtils',
        # 版本
        version='0.1.6',
        # 描述
        description="Common utils for python.",
        # 详细描述
        long_description=long_description,
        # 详细描述格式
        long_description_content_type='text/markdown',
        # 关键字
        keywords='common utils python base',
        # 作者
        author='Dong Qirui',
        # 作者邮箱
        author_email='QrCeric@Gmail.com',
        # 作者链接
        url='https://github.com/QrCer/qrcer_commons',
        packages=setuptools.find_packages(),
        # packages=setuptools.find_packages( exclude=['ez_setup', 'examples', 'tests'] ),
        # package name : [file name],
        include_package_data=True,
        zip_safe=False,
        # install_requires = ['docutils>=0.3'],
        install_requires=[  # 需求的第三方模块
                'redis',
                ],
        # entry_points={
        #         'console_scripts' : [  # 如果你想要以Linux命令的形式使用
        #                 'qc = utils.encode.automatic_switch_python_version:main'
        #                 ]
        #         },
        classifiers=[
                'Programming Language :: Python :: 2',
                'Programming Language :: Python :: 3',
                'License :: OSI Approved :: MIT License',
                'Operating System :: OS Independent',
                ],
        )
