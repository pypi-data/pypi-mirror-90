from distutils.core import setup

setup(
    name='module_my_first',  # 对外我们模块的名字
    version='1.0',  # 版本号
    description='这是第一个对外发布的模块，测试哦',  # 描述
    author='zengfu',  # 作者
    author_email='1434537427@qq.com',  # 作者邮箱
    py_modules=['module_my_first.module01']  # 要发布的模块
)
