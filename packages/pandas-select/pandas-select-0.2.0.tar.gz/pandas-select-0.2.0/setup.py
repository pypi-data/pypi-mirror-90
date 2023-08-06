# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pandas_select']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=0.25.3']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.5.0,<2.0.0'],
 'docs': ['pandera>=0.6.0,<0.7.0',
          'scikit-learn>=0.20',
          'furo>=2020.12.9-beta.21,<2021.0.0',
          'ipython>=7.12.0,<8.0.0',
          'Sphinx>=3.4.0,<4.0.0',
          'sphinx-panels>=0.5.2,<0.6.0',
          'xdoctest>=0.15.0,<0.16.0'],
 'tests': ['pandera>=0.6.0,<0.7.0',
           'scikit-learn>=0.20',
           'pytest>=6.2.1,<7.0.0']}

setup_kwargs = {
    'name': 'pandas-select',
    'version': '0.2.0',
    'description': 'Supercharged DataFrame indexing',
    'long_description': '==================================================\n``pandas-select``: Supercharged DataFrame indexing\n==================================================\n\n.. image:: https://github.com/jeffzi/pandas-select/workflows/tests/badge.svg\n   :target: https://github.com/jeffzi/pandas-select/actions\n   :alt: Github Actions status\n\n.. image:: https://codecov.io/gh/jeffzi/pandas-select/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/jeffzi/pandas-select\n   :alt: Coverage\n\n.. image:: https://readthedocs.org/projects/project-template-python/badge/?version=latest\n   :target: https://pandas-select.readthedocs.io/\n   :alt: Documentation status\n\n.. image:: https://img.shields.io/pypi/v/pandas-select.svg\n   :target: https://pypi.org/project/pandas-select/\n   :alt: Latest PyPI version\n\n.. image:: https://img.shields.io/pypi/pyversions/pandas-select.svg\n   :target: https://pypi.org/project/pandas-select/\n   :alt: Python versions supported\n\n.. image:: https://img.shields.io/pypi/l/pandas-select.svg\n   :target: https://pypi.python.org/pypi/pandas-select/\n   :alt: License\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Code style: black\n\n.. image:: https://img.shields.io/badge/style-wemake-000000.svg\n   :target: https://github.com/wemake-services/wemake-python-styleguide\n\n``pandas-select`` is a collection of DataFrame selectors that facilitates indexing\nand selecting data, fully compatible with pandas vanilla indexing.\n\nThe selector functions can choose variables based on their\n`name <https://pandas-select.readthedocs.io/en/latest/reference/label_selectors.html>`_,\n`data type <https://pandas-select.readthedocs.io/en/latest/reference/label_selection.html#data-type-selectors>`_,\n`arbitrary conditions <https://pandas-select.readthedocs.io/en/latest/reference/api/pandas_select.label.LabelMask.htmlk>`_,\nor any `combination of these <https://pandas-select.readthedocs.io/en/latest/reference/label_selection.html#logical-operators>`_.\n\n``pandas-select`` is inspired by the excellent R library `tidyselect <https://tidyselect.r-lib.org/reference/language.html>`_.\n\n.. installation-start\n\nInstallation\n------------\n\n``pandas-select`` is a Python-only package `hosted on PyPI <https://pypi.org/project/pandas-select/>`_.\nIt can be installed via `pip <https://pip.pypa.io/en/stable/>`_:\n\n.. code-block:: console\n\n   pip install pandas-select\n\n.. installation-end\n\nDesign goals\n------------\n\n* Fully compatible with the\n  `pandas.DataFrame <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_\n  ``[]`` operator and the\n  `pandas.DataFrame.loc <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html?highlight=loc#pandas.DataFrame.loc>`_\n  accessor.\n\n* Emphasise readability and conciseness by cutting boilerplate:\n\n.. code-block:: python\n\n   # pandas-select\n   df[AllNumeric()]\n   # vanilla\n   df.select_dtypes("number").columns\n\n   # pandas-select\n   df[StartsWith("Type") | "Legendary"]\n   # vanilla\n   df.loc[:, df.columns.str.startswith("Type") | (df.columns == "Legendary")]\n\n* Ease the challenges of `indexing with hierarchical index <https://pandas.pydata.org/pandas-docs/stable/user_guide/advanced.html#advanced-indexing-with-hierarchical-index>`_\n  and offers an alternative to `slicers <https://pandas.pydata.org/pandas-docs/stable/user_guide/advanced.html#advanced-mi-slicers>`_\n  when the labels cannot be listed manually.\n\n.. code-block:: python\n\n    # pandas-select\n    df_mi.loc[Contains("Jeff", axis="index", level="Name")]\n\n    # vanilla\n    df_mi.loc[df_mi.index.get_level_values("Name").str.contains("Jeff")]\n\n* Play well with machine learning applications.\n\n  - Respect the columns order.\n  - Allow *deferred selection* when the DataFrame\'s columns are not known in advance,\n    for example in automated machine learning applications.\n  - Offer integration with `sklearn <https://scikit-learn.org/stable/>`_.\n\n    .. code-block:: python\n\n        from pandas_select import AnyOf, AllBool, AllNominal, AllNumeric, ColumnSelector\n        from sklearn.compose import make_column_transformer\n        from sklearn.preprocessing import OneHotEncoder, StandardScaler\n\n        ct = make_column_transformer(\n           (StandardScaler(), ColumnSelector(AllNumeric() & ~AnyOf("Generation"))),\n           (OneHotEncoder(), ColumnSelector(AllNominal() | AllBool() | "Generation")),\n        )\n        ct.fit_transform(df)\n\n\nProject Information\n-------------------\n\n``pandas-select`` is released under the `BS3 <https://choosealicense.com/licenses/bsd-3-clause/>`_ license,\nits documentation lives at `Read the Docs <https://pandas-select.readthedocs.io/>`_,\nthe code on `GitHub <https://github.com/jeffzi/pandas-select>`_,\nand the latest release on `PyPI <https://pypi.org/project/pandas-select/>`_.\nIt is tested on Python 3.6+.\n',
    'author': 'Jean-Francois Zinque',
    'author_email': 'jzinque@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jeffzi/pandas-select/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<3.10',
}


setup(**setup_kwargs)
