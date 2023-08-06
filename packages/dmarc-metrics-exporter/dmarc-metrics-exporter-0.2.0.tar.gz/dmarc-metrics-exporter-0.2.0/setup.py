# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dmarc_metrics_exporter',
 'dmarc_metrics_exporter.model',
 'dmarc_metrics_exporter.model.tests',
 'dmarc_metrics_exporter.tests']

package_data = \
{'': ['*']}

install_requires = \
['aioimaplib>=0.7.18,<0.8.0',
 'dataclasses-serialization>=1.3.1,<2.0.0',
 'prometheus_client>=0.9.0,<0.10.0',
 'uvicorn[standard]>=0.13.2,<0.14.0',
 'xsdata>=20.12,<21.0']

setup_kwargs = {
    'name': 'dmarc-metrics-exporter',
    'version': '0.2.0',
    'description': 'Export Prometheus metrics from DMARC reports.',
    'long_description': None,
    'author': 'Jan Gosmann',
    'author_email': 'jan@hyper-world.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
