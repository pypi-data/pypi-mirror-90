# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_translator']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.3,<4.0.0',
 'nonebot2>=2.0.0-alpha.8,<3.0.0',
 'ujson>=4.0.1,<5.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-translator',
    'version': '2.0.0a8.post0',
    'description': 'Multi language tanslator worked with nonebot2',
    'long_description': '<!--\n * @Author       : Lancercmd\n * @Date         : 2020-12-15 10:21:55\n * @LastEditors  : Lancercmd\n * @LastEditTime : 2020-12-15 13:52:20\n * @Description  : None\n * @GitHub       : https://github.com/Lancercmd\n-->\n# nonebot_plugin_translator\n\n- 基于 [nonebot / nonebot2](https://github.com/nonebot/nonebot2)\n\n## 功能\n\n- 多语种翻译插件\n\n> 接口来自 [腾讯 AI 开放平台](https://ai.qq.com/product/nlptrans.shtml)\n\n## 准备工作\n\n- 在 [腾讯 AI 开放平台](https://ai.qq.com/console/) 新建应用，并从能力库接入 [机器翻译](https://ai.qq.com/console/capability/detail/7) 能力\n\n## 开始使用\n\n建议使用 poetry\n\n- 通过 poetry 添加到 nonebot2 项目的 pyproject.toml\n\n``` {.sourceCode .bash}\npoetry add nonebot-plugin-translator\n```\n\n- 也可以通过 pip 从 [PyPI](https://pypi.org/project/nonebot-plugin-translator/) 安装\n\n``` {.sourceCode .bash}\npip install nonebot-plugin-translator\n```\n\n- 在 nonebot2 项目中设置 `nonebot.load_plugin()`\n> 当使用 [nb-cli](https://github.com/nonebot/nb-cli) 添加本插件时，该条会被自动添加\n\n``` {.sourceCode .python}\nnonebot.load_plugin(\'nonebot_plugin_translator\')\n```\n\n- 参照下文在 nonebot2 项目的环境文件 `.env.*` 中添加配置项\n\n## 配置项\n\n- [腾讯 AI 开放平台](https://ai.qq.com/console/) 应用鉴权信息（必须）：\n\n  `tencent_app_id: int` 应用 APPID\n\n  `tencent_app_key: str` 应用 APPKEY\n\n``` {.sourceCode .bash}\n  tencent_app_id = 0123456789\n  tencent_app_key = ""\n```\n\n- 这样，就能够在 bot 所在群聊或私聊发送 `翻译` 或 `机翻` 使用了\n\n## 特别感谢\n\n- [Mrs4s / go-cqhttp](https://github.com/Mrs4s/go-cqhttp)\n- [nonebot / nonebot2](https://github.com/nonebot/nonebot2)\n\n## 优化建议\n\n如有优化建议请积极提交 Issues 或 Pull requests',
    'author': 'Lancercmd',
    'author_email': 'lancercmd@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Lancercmd/nonebot_plugin_translator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
