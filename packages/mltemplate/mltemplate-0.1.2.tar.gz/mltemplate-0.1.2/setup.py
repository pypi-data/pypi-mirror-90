# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mltemplate', 'mltemplate.cli']

package_data = \
{'': ['*'], 'mltemplate': ['scripts/*']}

entry_points = \
{'console_scripts': ['mltemplate = mltemplate.cli.__main__:main']}

setup_kwargs = {
    'name': 'mltemplate',
    'version': '0.1.2',
    'description': 'Templating tool with boiler plate code for building robust machine learning projects in python.',
    'long_description': '# ML Template\n\nML template is an easy to use tool to automate the boiler plate code for most machine learning projects.\n\nThis tool creates a user-oriented project architecture for machine learning projects.\n\nModify the code under `#TODO` comments in the template project repository to easily adapt the template to your use-case.\n\n# How to use it?\n1. Install the package as - `pip install mltemplate`\n2. Then, simply run `mltempate` from your terminal and follow the prompts\n\nAnd Voila! \n\nThis creates a project directory in your current folder similar to -\n```markdown\ntemplate\n├── Dockerfile.cpu\n├── Dockerfile.gpu\n├── Makefile\n├── pyproject.toml\n├── poetry.lock\n├── notebooks\n├── README.md\n└── template\n    ├── cli\n    │\xa0\xa0 ├── __init__.py\n    │\xa0\xa0 ├── __main__.py\n    │\xa0\xa0 ├── predict.py\n    │\xa0\xa0 └── train.py\n    ├── __init__.py\n    ├── models.py\n    ├── datasets.py\n    └── transforms.py\n```\nAll you have to do next is -\n1. Head to `template/datasets.py` and modify create a new dataset that will work for your use case\n2. Navigate to `template/models.py` and create a new model class with your sota (or not) architecture\n3. In `template/transforms.py` add transforms such as Normalizer, Denormalize etc.\n4. Follow the `TODO` steps in `template/cli/train.py` and `template/cli/predict.py` to make the necessary changes\n\nCheckout the `README.md` in the `template` directory for further instructions on how to train, predict and also monitor your loss plots using tensor board.\n\n# Future Work\nCurrently this package only supports boilerplate creation for ML projects in `pytorch`\n\nWe plan to support `tensorflow` in the future.\n\n## License\nCopyright © 2020 Sowmya Yellapragada\n\nDistributed under the MIT License (MIT).',
    'author': 'Sowmya Yellapragada',
    'author_email': 'sowmyayellapragada@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sowmyay/ml-project-template',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
