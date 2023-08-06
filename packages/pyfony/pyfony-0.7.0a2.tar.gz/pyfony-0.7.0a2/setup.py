# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyfony', 'pyfony.container']

package_data = \
{'': ['*'], 'pyfony': ['_config/*']}

install_requires = \
['console-bundle==0.3.0a2',
 'injecta>=0.8.11,<0.9.0',
 'logger-bundle==0.6.0a2',
 'pyfony-bundles==0.2.5a2']

entry_points = \
{'pyfony.bundle': ['autodetect = pyfony.PyfonyBundle:PyfonyBundle.autodetect']}

setup_kwargs = {
    'name': 'pyfony',
    'version': '0.7.0a2',
    'description': 'Dependency Injection powered framework',
    'long_description': "# Pyfony framework\n\nPyfony is a **Dependency Injection (DI) powered framework** written in Python greatly inspired by the [Symfony Framework](https://symfony.com/) in PHP & [Spring Framework](https://spring.io/projects/spring-framework) in Java.\n\nThe DI functionality is provided by the [Injecta Dependency Injection Container](https://github.com/pyfony/injecta).\n\nPyfony = **Injecta + bundles (extensions) API**\n\n## Installation\n\n```\n$ pip install pyfony\n```\n\n## Pyfony initialization\n\n(The following steps are covered in the [PyfonyBundleTest](src/pyfony/PyfonyBundleTest.py))\n\nTo start using Pyfony, create a simple `config_dev.yaml` file to define your DI services:\n\n```yaml\nparameters:\n  api:\n    endpoint: 'https://api.mycompany.com'\n\nservices:\n    mycompany.api.ApiClient:\n      arguments:\n        - '@mycompany.api.Authenticator'\n\n    mycompany.api.Authenticator:\n      class: mycompany.authenticator.RestAuthenticator\n      arguments:\n        - '%api.endpoint%'\n        - '%env(API_TOKEN)%'\n```\n\nThen, initialize the container:\n\n```python\nfrom injecta.config.YamlConfigReader import YamlConfigReader\nfrom pyfony.Kernel import Kernel\nfrom pyfonybundles.loader import pyfonyBundlesLoader\n\nappEnv = 'dev'\n\nkernel = Kernel(\n    appEnv,\n    '/config/dir/path', # must be directory, not the config_dev.yaml file path!\n    pyfonyBundlesLoader.loadBundles(),\n    YamlConfigReader()\n)\n\ncontainer = kernel.initContainer()\n```\n\nUse `container.get()` to finally retrieve your service:\n\n```python\nfrom mycompany.api.ApiClient import ApiClient\n\napiClient = container.get('mycompany.api.ApiClient') # type: ApiClient   \napiClient.get('/foo/bar')\n```\n\n## Advanced examples\n\n1. [Advanced services configuration using Injecta](https://github.com/pyfony/injecta/blob/master/README.md)\n1. [Extending Pyfony with bundles](docs/bundles.md)\n",
    'author': 'Jiri Koutny',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pyfony/pyfony',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.3,<3.8.0',
}


setup(**setup_kwargs)
