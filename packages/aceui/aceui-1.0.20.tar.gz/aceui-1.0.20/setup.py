# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aceui',
 'aceui.base',
 'aceui.lib',
 'aceui.scaffold',
 'aceui.scaffold.pages',
 'aceui.scaffold.testCase']

package_data = \
{'': ['*'], 'aceui': ['config/*'], 'aceui.scaffold': ['data/*']}

install_requires = \
['Pillow==5.3.0',
 'PyAutoIt==0.6.0',
 'PyYAML==5.1.1',
 'ddt==1.1.3',
 'requests==2.25.0',
 'selenium==3.141.0',
 'xlrd==1.2.0',
 'xlutils==2.0.0',
 'xlwt==1.3.0']

entry_points = \
{'console_scripts': ['ace = aceui.cli:run_min', 'aceui = aceui.cli:run_min']}

setup_kwargs = {
    'name': 'aceui',
    'version': '1.0.20',
    'description': '基于Selenium的UI自动化测试框架',
    'long_description': '\ufeff# AceUI\n\nAceUI是基于Selenium的UI自动化测试框架。\n\n\n\n\n\n\n  \n### 通过poetry工具打包\n\n- poetry build\n\n- poetry config repositories.testpypi https://pypi.org/project/aceui\n\n- poetry publish  输入pypi用户名和密码',
    'author': '天枢',
    'author_email': 'lengyaohui@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/HttpTesting/aceui',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
