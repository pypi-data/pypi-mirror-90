# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bridge_sim',
 'bridge_sim.bridges',
 'bridge_sim.configs',
 'bridge_sim.creep',
 'bridge_sim.internal',
 'bridge_sim.internal.make',
 'bridge_sim.internal.make.plot',
 'bridge_sim.internal.make.plot.contour',
 'bridge_sim.internal.plot',
 'bridge_sim.internal.plot.geometry',
 'bridge_sim.internal.validate',
 'bridge_sim.model',
 'bridge_sim.plot',
 'bridge_sim.shrinkage',
 'bridge_sim.sim',
 'bridge_sim.sim.build',
 'bridge_sim.sim.model',
 'bridge_sim.sim.responses',
 'bridge_sim.sim.run',
 'bridge_sim.sim.run.opensees',
 'bridge_sim.sim.run.opensees.build',
 'bridge_sim.sim.run.opensees.build.d3',
 'bridge_sim.sim.run.opensees.convert',
 'bridge_sim.sim.run.opensees.parse',
 'bridge_sim.temperature',
 'bridge_sim.traffic',
 'bridge_sim.vehicles']

package_data = \
{'': ['*']}

install_requires = \
['click==7.1.2',
 'colorama==0.4.3',
 'findup==0.3.0',
 'matplotlib==3.2.1',
 'numba==0.50.0rc1',
 'numpy==1.19.0rc2',
 'pandas==1.0.4',
 'pathos==0.2.5',
 'portalocker==1.7.0',
 'scipy==1.5.0rc1',
 'sklearn==0.0',
 'termcolor==1.1.0']

setup_kwargs = {
    'name': 'bridge-sim',
    'version': '0.0.8.9',
    'description': 'A Python library for concrete slab bridge simulation',
    'long_description': None,
    'author': 'Jeremy Barisch-Rooney',
    'author_email': 'jerbaroo.work@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jerbaroo/bridge-sim',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
