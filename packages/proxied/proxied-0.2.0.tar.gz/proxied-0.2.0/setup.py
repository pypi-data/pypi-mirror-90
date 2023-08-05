# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['proxy']
setup_kwargs = {
    'name': 'proxied',
    'version': '0.2.0',
    'description': 'A simple to use proxy for python objects',
    'long_description': 'proxied\n-------\nproxied package can be use to defer initialization of object.\n\nSuppose we have:\n\n**__init__.py**\n\n.. code-block:: python\n\n    from config import Config, load_config\n\n    config: Config = None\n\n    def init_app():\n        config = load_config()\n\nIf we try to import config in another file, i.e.\n\n**cool_staff.py**\n\n.. code-block:: python\n\n    from . import config\n\n    ...\n\n    init_staff(config.db_url)\n\nWe will end up importing None. So, we will be forced to\nmake import not at the top of the file.\n\n**Here comes the proxied package**\n\n**__init__.py**\n\n.. code-block:: python\n\n    from typing import Union\n    from proxy import Proxy\n    from config import Config, load_config\n\n    config: Union[Config, Proxy] = Proxy()\n\n    def init_app():\n        config.set_inner(load_config())\n\nNow we can easily import config at the top of the file work with\nproxy object as it was the object of type Config.\n\nInstallation\n------------\n\n.. code-block::\n\n    pip install proxied\n\nProxy\n-----------------------\nProxy class can be initialized with inner or inner_constructor.\nIf inner_constructor is supplied, then it will be called once,\nand the result will be cached.\n\nIf Proxy class is initialized without inner and inner_constructor,\nthe inner should be set later with a help of ``proxy.set_inner`` method.\n\n.. code-block:: python\n\n    from proxy import Proxy\n    proxy = Proxy()\n    proxy.set_inner({})\n    proxy["test_key"] = 10\n\n\nIt\'s possible to set values for multiple proxies.\n\n.. code-block:: python\n\n    from proxy import Proxy\n    proxies = [Proxy(), Proxy(), Proxy(), Proxy()]\n    values = [10, 11, list(), dict()]\n    Proxy.set_proxies(proxies, values)\n\nThere is a check, if proxy is initialized with proxied value\n\n.. code-block:: python\n\n    from proxy import Proxy\n    proxy = Proxy()\n\n    if not proxy.initialized:\n        data = get_needed_data(...)\n        proxy.set_inner(data)\n\nExample\n-------\n.. code-block:: python\n\n    from proxy import Proxy\n    class NotAvailableDuringImport:\n        @property\n        def data(self):\n            return "Not Available during import"\n\n\n    proxy: Union[NotAvailableDuringImport, Proxy] = Proxy()\n    proxy.set_inner(NotAvailableDuringImport)\n    assert proxy.data == "Not Available during import"\n\nLicense\n-------\n\nCopyright Oleksii Petrenko, 2020.\n\nDistributed under the terms of the `MIT`_ license,\njson_modify is free and open source software.\n\n.. _`MIT`: https://github.com/Enacero/proxied/blob/master/LICENSE',
    'author': 'Oleksii Petrenko',
    'author_email': 'oleksiiypetrenko@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Enacero/proxied',
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
