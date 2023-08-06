# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bna']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'pyotp>=2.4.0,<3.0.0']

setup_kwargs = {
    'name': 'bna',
    'version': '5.0.1',
    'description': 'Blizzard Authenticator and OTP library in Python',
    'long_description': '# python-bna\n[![Build Status](https://api.travis-ci.org/jleclanche/python-bna.svg?branch=master)](https://travis-ci.org/jleclanche/python-bna)\n\n## Requirements\n\n- Python 3.6+\n\n\n## Command-line usage\n\nbna is a command line interface to the python-bna library. It can store\nand manage multiple authenticators, as well as create new ones.\n\n\nRemember: Using an authenticator on the same device as the one you log in with\nis less secure than keeping the devices separate. Use this at your own risk.\n\nConfiguration is stored in `~/.config/bna/bna.conf`. You can pass a\ndifferent config path with `bna --config=~/.bna.conf` for example.\n\n\n### Creating a new authenticator\n\n    $ bna new\n\nIf you do not already have an authenticator, it will be set as default.\nYou can pass `--set-default` otherwise.\n\n\n### Getting an authentication token\n\n    $ bna\n    01234567\n    $ bna EU-1234-1234-1234\n    76543210\n\n\n### Getting an authenticator\'s restore code\n\n    $ bna show-restore-code\n    Z45Q9CVXRR\n    $ bna restore EU-1234-1234-1234 ABCDE98765\n    Restored EU-1234-1234-1234\n\n\n### Getting an OTPAuth URL\n\nTo display the OTPAuth URL (used for setup QR Codes):\n\n    $ bna show-url\n    otpauth://totp/Blizzard:EU123412341234:?secret=ASFAS75ASDF75889G9AD7S69AS7697AS&issuer=Blizzard&digits=8\n\nNow paste this to your OTP app, or convert to QRCode and scan, or\nmanually enter the secret.\n\nThis is compatible with standard TOTP clients and password managers such as:\n- [andOTP](https://play.google.com/store/apps/details?id=org.shadowice.flocke.andotp) (Android),\n- [KeepassXC](https://keepassxc.org/) (Cross-platform)\n- [1Password](https://1password.com/) (Cross-platform)\n\n\n#### Getting a QR code\n\nTo encode to a QRCode on your local system install \\\'qrencode\\\'\n\nFor a PNG file saved to disk :\n\n    $ bna show-url | qrencode -o ~/BNA-qrcode.png\n    # Scan QRCode\n    $ rm ~/BNA-qrcode.png\n\nOr to attempt ot display QRCode in terminal as text output :\n\n    $ bna --otpauth-url | qrencode -t ANSI\n\n\n## Python library usage\n\n### Requesting a new authenticator\n\n```py\nimport bna\ntry:\n    # region is EU or US\n    # note that EU authenticators are valid in the US, and vice versa\n    serial, secret = bna.request_new_serial("US")\nexcept bna.HTTPError as e:\n    print("Could not connect:", e)\n```\n\n### Getting a token\n\n```py\n    # Get and print a token using PyOTP\n    from pyotp import TOTP\n    totp = TOTP(secret, digits=8)\n    print(totp.now())\n```\n',
    'author': 'Jerome Leclanche',
    'author_email': 'jerome@leclan.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jleclanche/python-bna',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
