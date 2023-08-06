"""
使用方式:

在配置文件中:
```python
from django_qiyu_utils.settings import *
```
"""

from .env import EnvHelper

# 只需要导出有用的变量
#
# Django 项目导出的配置项
#
__all__ = ["DEBUG"]

# 只有设置了 DJANGO_DEV 环境变量,
# 才   是在 `开发` 环境中运行
# 否则 是在 `线上` 环境中运行
# 在开发的时候, 请务必设置 DJANGO_DEV 环境变量
if EnvHelper.in_prod():  # 先检测线上
    DEBUG = False
elif EnvHelper.in_dev() or EnvHelper.in_test():  # 开发 & 测试 环境
    DEBUG = True
else:  # 默认 不使用 调试
    DEBUG = False
