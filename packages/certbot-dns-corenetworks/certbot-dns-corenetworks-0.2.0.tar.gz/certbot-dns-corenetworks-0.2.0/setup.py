# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['certbot_dns_corenetworks',
 'certbot_dns_corenetworks.test',
 'certbot_dns_corenetworks.test.unit']

package_data = \
{'': ['*']}

install_requires = \
['acme>=1.10.1,<2.0.0',
 'certbot>=1.10.1,<2.0.0',
 'corenetworks>=0.1.4,<0.2.0',
 'parsedatetime>=2.6,<3.0',
 'zope.interface>=5.2.0,<6.0.0']

entry_points = \
{'certbot.plugins': ['dns-corenetworks = '
                     'certbot_dns_corenetworks.dns_corenetworks:Authenticator']}

setup_kwargs = {
    'name': 'certbot-dns-corenetworks',
    'version': '0.2.0',
    'description': 'Core Networks DNS Authenticator plugin for Certbot.',
    'long_description': "# certbot-dns-corenetworks\n\n[![Build Status](https://img.shields.io/drone/build/thegeeklab/certbot-dns-corenetworks?logo=drone)](https://cloud.drone.io/thegeeklab/certbot-dns-corenetworks)\n[![Python Version](https://img.shields.io/pypi/pyversions/certbot-dns-corenetworks.svg)](https://pypi.org/project/certbot-dns-corenetworks/)\n[![PyPi Status](https://img.shields.io/pypi/status/certbot-dns-corenetworks.svg)](https://pypi.org/project/certbot-dns-corenetworks/)\n[![PyPi Release](https://img.shields.io/pypi/v/certbot-dns-corenetworks.svg)](https://pypi.org/project/certbot-dns-corenetworks/)\n[![Codecov](https://img.shields.io/codecov/c/github/thegeeklab/certbot-dns-corenetworks)](https://codecov.io/gh/thegeeklab/certbot-dns-corenetworks)\n[![GitHub contributors](https://img.shields.io/github/contributors/thegeeklab/certbot-dns-corenetworks)](https://github.com/thegeeklab/certbot-dns-corenetworks/graphs/contributors)\n[![License: MIT](https://img.shields.io/github/license/thegeeklab/certbot-dns-corenetworks)](https://github.com/thegeeklab/certbot-dns-corenetworks/blob/main/LICENSE)\n\n## Install\n\nInstall this package via pip in the same python environment where you installed your certbot.\n\n```console\npip install certbot-dns-corenetworks\n```\n\n## Usage\n\nTo start using DNS authentication for the Core Networks DNS API, pass the following arguments on certbot's command line:\n\n| Option                                                            | Description                                      |\n| ----------------------------------------------------------------- | ------------------------------------------------ |\n| `--authenticator dns-corenetworks`       | select the authenticator plugin (Required)       |\n| `--dns-corenetworks-credentials`         | Hetzner DNS API credentials INI file. (Required) |\n| `--dns-corenetworks-propagation-seconds` | Seconds to wait for the TXT record to propagate  |\n\n## Credentials\n\n```ini\ndns_corenetworks_username = asaHB12r\ndns_corenetworks_password = secure_passwor\n```\n\n## Examples\n\nTo acquire a certificate for `example.com`\n\n```bash\ncertbot certonly \\\n --authenticator dns-corenetworks \\\n --dns-corenetworks-credentials /path/to/my/credentials.ini \\\n -d example.com\n```\n\nTo acquire a certificate for `*.example.com`\n\n```bash\ncertbot certonly \\\n    --authenticator dns-corenetworks \\\n    --dns-corenetworks-credentials /path/to/my/credentials.ini \\\n    -d '*.example.com'\n```\n\n## Contributors\n\nSpecial thanks goes to all [contributors](https://github.com/thegeeklab/certbot-dns-corenetworks/graphs/contributors). If you would like to contribute,\nplease see the [instructions](https://github.com/thegeeklab/certbot-dns-corenetworks/blob/main/CONTRIBUTING.md).\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE](https://github.com/thegeeklab/certbot-dns-corenetworks/blob/main/LICENSE) file for details.\n",
    'author': 'Robert Kaussow',
    'author_email': 'mail@thegeeklab.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thegeeklab/certbot-dns-corenetworks/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.0,<4.0.0',
}


setup(**setup_kwargs)
