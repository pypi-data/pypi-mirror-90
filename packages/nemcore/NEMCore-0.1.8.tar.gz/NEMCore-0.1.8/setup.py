# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nemcore', 'nemcore.types']

package_data = \
{'': ['*']}

install_requires = \
['cachetools>=4.0,<5.0',
 'importlib-metadata>=3.3.0,<4.0.0',
 'pycryptodomex>=3.9,<4.0',
 'requests>=2.22.0,<3.0.0']

setup_kwargs = {
    'name': 'nemcore',
    'version': '0.1.8',
    'description': 'NetEase Cloud Music api client',
    'long_description': "# NetEase Cloud Music ApiClient\n\n![python-version](https://img.shields.io/pypi/pyversions/nemcore)\n![pypi-version](https://img.shields.io/pypi/v/nemcore)\n[![Documentation Status](https://readthedocs.org/projects/nemcore/badge/?version=latest)](https://nemcore.readthedocs.io/en/latest/?badge=latest)\n![github-issues](https://img.shields.io/github/issues-raw/nnnewb/nemcore)\n![license](https://img.shields.io/github/license/nnnewb/nemcore)\n![downloads](https://img.shields.io/pypi/dd/nemcore)\n\n网易云音乐核心 API 客户端。\n\n这个项目的目的是抽离一个干净的 API Client，便于二次开发和维护。\n\n主要代码来自[NetEase-MusicBox](https://github.com/darknessomi/musicbox/)，非常感谢每一位该项目的贡献者。\n\n**警告，目前 API 尚未稳定，不保证兼容性。万一有新点子说不定就会改。**\n\n此外欢迎 code review 和 pull request。\n\n## 安装\n\n使用 pip 安装\n\n```shell script\npip install NEMCore\n```\n\n文档生成需要额外依赖项\n\n```shell script\npip install NEMCore[docs]\n```\n\n单元测试需要额外依赖\n\n```shell script\npip install NEMCore[test]\n```\n\n## 使用\n\n### quickstart\n\n```python\nfrom nemcore.api import NetEaseApi\n\nnetease = NetEaseApi(cookie_path='./cookies')\nnetease.login('cloudmusic@163.com', 'password')\n\n# 获取我的歌单\nplaylists = netease.get_user_playlist()\n\n# 获取日推\nrecommend = netease.get_recommend_songs()\n\n# 签到\nnetease.daily_task()\n```\n\n详细的 api 文档和快速开始请参考[这里](https://nemcore.readthedocs.io/en/latest/)。\n\n## v1.0 开发计划\n\n- [x] 添加测试用例\n- [x] 规范命名和返回值结构\n- [x] 提供可配置的缓存(是否持久化，缓存有效时间等)\n- [x] 提供文档，挂在[readthedocs.io](https://nemcore.readthedocs.io/en/latest/)上。\n- [x] 重构简化 api 和实现。\n- [ ] 提供助手函数，实现一些常用操作\n- [x] 移除 python2 支持(`__future__`等)，迁移到 python3.6+\n- [ ] 支持异步(考虑`aiohttp`)\n\n## changelog\n\n### current\n\n### 0.1.8\n\n- fix ImportError about filelock\n\n### 0.1.7\n\n**BREAKING CHANGE !**\n\n- API 返回类型修改和标注\n\n### 0.1.6\n\n- 修复 `login` 接口登录失败错误\n\n### 0.1.5\n\n本版本主要修复影响运行的问题，把包构建从`poetry`改为`setuptools`。\n\n在`poetry`可用性足够之前不会用它了。\n\n- 修复 `from cachetools.ttl import default_timer` 失败的问题\n- 从`poetry`迁移到`setuptools`\n\n有一些已知的问题如下。\n\n- `login` 会抛出错误代码 `501`，暂时没找到好办法处理。\n\n### 0.1.4\n\n本版本主要是对代码进行重构，将核心 Api 类清晰化，解耦无关逻辑，简化了使用。\n\n此外，提供了比较详细的入门文档，帮助使用者快速了解使用方式和 api 的响应内容。\n\n不过 api 文档不是很好，需要改进。\n\n- `nemcore.netease` 模块重命名成 `nemcore.api`\n- `nemcore.netease.NetEase` 重命名成 `nemcore.api.NetEaseApi`\n- 删除 `nemcore.conf` 模块\n- 删除 `nemcore.storage` 模块\n- 删除 `nemcore.parser` 模块\n- 删除 `nemcore.pdict` 模块\n- 添加 sphinx 文档和快速开始指引，文档已经挂到了 readthedocs.io\n\n### 0.1.3\n\n- 支持缓存。基于`pickle`和`cachetools`实现，可配置缓存时间和是否持久化\n",
    'author': 'weak_ptr',
    'author_email': 'weak_ptr@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nnnewb/nemcore',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
