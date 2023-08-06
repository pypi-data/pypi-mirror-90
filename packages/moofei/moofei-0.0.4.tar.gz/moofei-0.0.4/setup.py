# -*- coding: utf-8

import os
from distutils.core import setup, Extension
from distutils.sysconfig import get_python_lib

install_requires  = [ # 第三方依赖
        "chardet"
    ]
    
setup(
    name='moofei',  # 安装包名
    version='0.0.4',  # 打包安装软件的版本号
    description="find,valid,tree,date,db,waf By mufei",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author= 'mufei', # maintainer="None",  # 提供与包相关的其他维护者的名字
    author_email= 'ypdh@qq.com', # maintainer_email="None",  # 其他维护者的邮箱
    url="http://www.mufei.ltd",  # 包相关网站主页的的访问地址
    download_url="",  # 下载安装包(zip , exe)的url
    keywords="moofei mufei find valid tree date db waf",
    #py_modules=['package'],  # 设置打包模块，可以多个
    
    packages   = ['moofei','moofei.tests','moofei.find','moofei.valid'],          # 要打包的项目文件夹
    package_dir= {"moofei": "lib/moofei" },
    # 对于C,C++,Java 等第三方扩展模块一起打包时，需要指定扩展名、扩展源码、以及任何编译/链接 要求（包括目录、链接库等）
    ext_modules = [Extension('moofei._find',['src/_find.c']), 
                   Extension('moofei.path',['src/path.c']), 
                   Extension('moofei._ftp',['src/_ftp.c']),
                   Extension('moofei._valid',['src/_valid.c']),
                   Extension('moofei._db',['src/_db.c']),
                   ],
    requires = install_requires,
    install_requires=install_requires,
    setup_requires=install_requires,
    include_package_data = True, #Unknown
    #data_files=[ ###(会在python37/下创建文件夹) 打包时需要打包的数据文件，如图片，配置文件等    
        #("static", [r"lib/moofei/static/utf8.txt", "lib/moofei/static/logo.png"]),
    #], 
    #package_data={ # 如果是包的子目录下，则需要手动添加
    #    'moofei.static': ['lib/moofei/static/*.txt']
    #},
    python_requires = ">=2.6, !=3.0.*, !=3.1.*, !=3.2.*",  #Unknown Python版本依赖 
    license = "BSD",
    
)

