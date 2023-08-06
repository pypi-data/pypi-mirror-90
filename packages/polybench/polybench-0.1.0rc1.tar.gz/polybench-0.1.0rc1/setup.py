# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polybench', 'polybench.solvers']

package_data = \
{'': ['*'],
 'polybench.solvers': ['reform/*',
                       'reform/src/*',
                       'rings/*',
                       'rings/config/*',
                       'rings/gradle/wrapper/*',
                       'rings/src/main/java/com/github/tueda/polybench/rings/*']}

install_requires = \
['colorama>=0.4.4,<0.5.0',
 'colorlog>=4.6.2,<5.0.0',
 'importlib-metadata>=3.3.0,<4.0.0',
 'importlib-resources>=4.1.1,<5.0.0',
 'matplotlib>=3.3.3,<4.0.0',
 'pandas>=1.1.5,<2.0.0',
 'pretty-errors>=1.2.19,<2.0.0',
 'psutil>=5.8.0,<6.0.0',
 'py-cpuinfo>=7.0.0,<8.0.0',
 'symengine>=0.6.1,<0.7.0',
 'toml>=0.10.2,<0.11.0',
 'typing-extensions>=3.7.4,<4.0.0']

entry_points = \
{'console_scripts': ['polybench = polybench.__main__:entry_point']}

setup_kwargs = {
    'name': 'polybench',
    'version': '0.1.0rc1',
    'description': 'Multivariate polynomial arithmetic benchmark tests.',
    'long_description': 'polybench\n=========\n\n[![Test](https://github.com/tueda/polybench/workflows/Test/badge.svg?branch=master)](https://github.com/tueda/polybench/actions?query=branch:master)\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/tueda/polybench.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/tueda/polybench/context:python)\n\nMultivariate polynomial arithmetic benchmark tests.\n\nMany scientific and engineering applications utilise multivariate polynomial\narithmetic in their algorithms and solutions. Here we provide a set of\nbenchmark tests for often-used operations in multivariate polynomial\narithmetic:\n\n- Greatest common divisor\n- Factorisation\n\n\nRequirements\n------------\n\n- [Python](https://www.python.org/) >= 3.6.1\n\nYou also need at least one or more tools to be benchmarked.\nThey are (in alphabetical order):\n\n- [Fermat](https://home.bway.net/lewis/)\n- [FORM](https://www.nikhef.nl/~form/):\n  if not available in the system, then\n  a [release binary](https://github.com/vermaseren/form/releases)\n  will be automatically downloaded.\n- [Mathematica](https://www.wolfram.com/mathematica/)\n- [reFORM](https://reform.readthedocs.io/en/latest/):\n  automatically downloaded\n  (requires [Rust](https://www.rust-lang.org/) >= 1.36).\n- [Rings](https://ringsalgebra.io/):\n  automatically downloaded\n  (requires [JDK](https://www.oracle.com/technetwork/java/) >= 8).\n- [Singular](https://www.singular.uni-kl.de/)\n\n\nGet started\n-----------\n\nClone this repository and try to run the `run.sh` script:\n\n```sh\ngit clone https://github.com/tueda/polybench.git\ncd polybench\n./run.sh --all\n```\n\nWhen starting the script for the first time, it automatically sets up\na virtual environment for required Python packages so that it will not dirty\nyour environment. Some of the tools are provided as libraries registered in\npublic package registries, so the first run takes some time to download,\ncompile and link them with test binaries. After testing, a CSV file and\ncomparison plots will be generated.\n\nFor practical benchmarking, configuration parameters should be set\nadequately. See the help message shown by\n\n```sh\n./run.sh --help\n```\n\nYou can also use [Poetry](https://python-poetry.org/)\nor [Docker](https://www.docker.com/) with this repository.\n\n\nLicense\n-------\n\n[MIT](https://github.com/tueda/polybench/blob/master/LICENSE)\n',
    'author': 'Takahiro Ueda',
    'author_email': 'tueda@st.seikei.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tueda/polybench',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
