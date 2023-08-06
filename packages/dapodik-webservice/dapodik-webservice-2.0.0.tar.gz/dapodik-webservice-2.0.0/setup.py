# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dapodik_webservice',
 'dapodik_webservice.models',
 'dapodik_webservice.models.ptk',
 'dapodik_webservice.models.rombongan_belajar']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.3.0,<21.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'dapodik-webservice',
    'version': '2.0.0',
    'description': 'SDK Python Web Service aplikasi Dapodik',
    'long_description': "# dapodik-webservice\n\n[![dapodik-webservice - PyPi](https://img.shields.io/pypi/v/dapodik-webservice)](https://pypi.org/project/dapodik-webservice/)\n\nSDK Python Web Service aplikasi Dapodik\n\n## Install\n\nPastikan python 3.7 terinstall, kemudian jalankan perintah di bawah dalam Command Prompt atau Powershell (di Windows + X):\n\n```bash\npip install --upgrade dapodik-webservice\n```\n\n## Penggunaan\n\nUntuk menggunakan modul ini silahkan buat token Web Service Dapodik terlebih dahulu di pengaturan Dapodik.\n\n```python\nfrom dapodik_webservice import DapodikWebservice\n\ntoken = 'token webservice'\nnpsn = '12345678'\n\ndw = DapodikWebservice(token, npsn)\n\nsekolah = dw.sekolah\n\nprint(sekolah.nama)\n\n```\n\n## Donasi\n\nJika anda ingin melakukan donasi untuk kami, bisa menghubungi kami melalui [WhatsApp](https://wa.me/6287725780404) ataupun [Telegram](https://t.me/hexatester).\n\n## Legal / Hukum\n\nKode ini sama sekali tidak berafiliasi dengan, diizinkan, dipelihara, disponsori atau didukung oleh Kemdikbud atau afiliasi atau anak organisasinya. Ini adalah perangkat lunak yang independen dan tidak resmi. Gunakan dengan risiko Anda sendiri.\n",
    'author': 'hexatester',
    'author_email': 'habibrohman@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://dapodix.github.io/dapodik-webservice/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
