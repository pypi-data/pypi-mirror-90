# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastq_statistic']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.3,<4.0.0',
 'numpy>=1.19.5,<2.0.0',
 'pandas>=1.2.0,<2.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['fastq-statistic = fastq_statistic.main:app']}

setup_kwargs = {
    'name': 'fastq-statistic',
    'version': '0.1.2',
    'description': '',
    'long_description': 'Fastq Statistic\n===============\nCalculate statistics for Fastq Files.  \n\n# Requirement\nPython: 3.8 or upper  \n\n# Install\nDownload the release whl file.  \n\n```bash\nuser@linux:~$ python3.8 -m pip install ./fastq_statistic-0.1.1-py3-none-any.whl\n```\n\n# Usage\n```bash\nuser@linux:~$ fastq-statistic --help\nUsage: fastq-statistic [OPTIONS] READ1 [READ2]\n\nArguments:\n  READ1    Read1 fastq path or fastq path  [required]\n  [READ2]  Read2 filepath or None\n\nOptions:\n  --sampleid TEXT                 SampleID, default is the first item of\n                                  filename splited by underscore(_)\n\n  --result PATH                   Result csv file name, plot with use the same\n                                  name.\n\n  --help                          Show this message and exit.\n\n```',
    'author': 'Mao Yibo',
    'author_email': 'maoyibo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
