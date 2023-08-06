# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tess_ephem']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=4.1,<5.0',
 'astroquery>=0.4.1,<0.5.0',
 'numpy>=1.19.4,<2.0.0',
 'pandas>=1.1.4,<2.0.0',
 'scipy>=1.5.4,<2.0.0',
 'tess-locator>=0.2.0']

setup_kwargs = {
    'name': 'tess-ephem',
    'version': '0.1.1',
    'description': 'Where are Solar System objects located in TESS FFI data?',
    'long_description': 'tess-ephem\n==========\n\n\n**Where are Solar System objects located in TESS FFI data?**\n\n|pypi| |pytest| |black| |flake8| |mypy|\n\n.. |pypi| image:: https://img.shields.io/pypi/v/tess-ephem\n                :target: https://pypi.python.org/pypi/tess-ephem\n.. |pytest| image:: https://github.com/SSDataLab/tess-ephem/workflows/pytest/badge.svg\n.. |black| image:: https://github.com/SSDataLab/tess-ephem/workflows/black/badge.svg\n.. |flake8| image:: https://github.com/SSDataLab/tess-ephem/workflows/flake8/badge.svg\n.. |mypy| image:: https://github.com/SSDataLab/tess-ephem/workflows/mypy/badge.svg\n\n`tess-ephem` is a user-friendly package which enables users to compute the positions of Solar System objects -- asteroids, comets, and planets --\nin the data archive of NASA\'s TESS Space Telescope.\n\nInstallation\n------------\n\n.. code-block:: bash\n\n    python -m pip install tess-ephem\n\n\nExample use\n-----------\n\ntess-ephem allows you to search the entire archive of TESS FFI\'s for the presence\nof a known minor planet, and obtain the result as a Pandas DataFrame.\nFor example:\n\n.. code-block:: python\n\n    >>> from tess_ephem import ephem\n    >>> ephem("Sedna")\n                             sector  camera  ccd       column          row\n    time\n    2018-11-16 00:00:00.000       5       1    4  1543.312296  1102.821559\n    2018-11-17 00:00:00.000       5       1    4  1545.160910  1102.880825\n    2018-11-18 00:00:00.000       5       1    4  1547.011351  1102.934375\n    ...\n    2018-12-09 00:00:00.000       5       1    4  1584.585407  1102.239292\n    2018-12-10 00:00:00.000       5       1    4  1586.245261  1102.132304\n    2018-12-11 00:00:00.000       5       1    4  1587.906380  1102.012091\n\n\nYou can also obtain the ephemeris for one or more specific times\nby passing the `time` parameter:\n\n.. code-block:: python\n\n    >>> ephem("Sedna", time="2018-11-21 17:35:00")\n                             sector  camera  ccd       column          row\n    time\n    2018-11-21 17:35:00.000       5       1    4  1553.887838  1103.048431\n\n\nAdditional physical parameters can be obtained by passing the `verbose=True` parameter:\n\n.. code-block:: python\n\n    >>> ephem("Sedna", time="2018-11-21 17:35:00", verbose=True)\n                             sector  camera  ccd       column          row  pixels_per_hour        ra      dec    vmag  sun_distance  obs_distance  phase_angle\n    time\n    2018-11-21 17:35:00.000       5       1    4  1553.887838  1103.048431         0.074054  57.05786  7.63721  20.612     84.942885     83.975689       0.1419\n\n\nFinally, using the companion `tess-locator <https://github.com/SSDataLab/tess-locator>`_\npackage, you can convert the TESS pixel coordinates directly to FFI filenames and urls:\n\n.. code-block:: python\n\n    >>> from tess_locator import TessCoordList\n    >>> df = ephem("Sedna", time=["2018-11-21 17:35:00", "2018-11-22 17:35:00"])\n    >>> TessCoordList.from_pandas(df).get_images()\n    List of 2 images\n    ↳[TessImage(filename=\'tess2018325165939-s0005-1-4-0125-s_ffic.fits\', begin=\'2018-11-21 17:07:46\', end=\'2018-11-21 17:37:46\')\n      TessImage(filename=\'tess2018326165939-s0005-1-4-0125-s_ffic.fits\', begin=\'2018-11-22 17:07:46\', end=\'2018-11-22 17:37:46\')]\n',
    'author': 'Geert Barentsen',
    'author_email': 'hello@geert.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SSDataLab/tess-ephem',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
