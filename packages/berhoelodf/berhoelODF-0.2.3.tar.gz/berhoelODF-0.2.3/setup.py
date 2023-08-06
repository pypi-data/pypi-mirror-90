# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['berhoel', 'berhoel.odf', 'berhoel.odf.test']

package_data = \
{'': ['*']}

install_requires = \
['lxml']

setup_kwargs = {
    'name': 'berhoelodf',
    'version': '0.2.3',
    'description': 'Lightweight and limited access to odf files using lxml.',
    'long_description': '``berhoelODF``\n==============\n\nLightweight and limited access to odf files using lxml.\n\nIt is just used by me for a limited project of converting a\nspreadsheet to ``Django`` data. For me this package works much faster\nthan ``odfpy``. Just loading my 5.7MB ods file took 1.5 minutes. This\npackage is based on ``lxml``, and ``lxml`` parses the XML in 2\nseconds, the whole processing to ``Django`` takes about 1.5 minutes.\n\nIf you have other requirements, the code should be easily extensible.\n\nInstallation\n------------\n\n``pip install berhoelodf``\n\nAvailability\n~~~~~~~~~~~~\n\nThe latest version should be available at my `GitLab\n<https://gitlab.com/berhoel/python/berhoelODF.git>`_ repository, the\npackage is avaliable at `pypi <https://pypi.org/project/berhoelODF/>`_\nvia ``pip install berhoelodf``.\n\nDocumentation\n~~~~~~~~~~~~~\n\nDocumentation is hosted on `höllmanns.de <https://www.höllmanns.de/python/berhoelODF/>`_.\n',
    'author': 'Berthold Höllmann',
    'author_email': 'berthold-gitlab@xn--hllmanns-n4a.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://python.xn--hllmanns-n4a.de/berhoelODF/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.8',
}


setup(**setup_kwargs)
