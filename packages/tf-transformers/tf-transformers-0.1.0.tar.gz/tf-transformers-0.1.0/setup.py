# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tf_transformers',
 'tf_transformers.activations',
 'tf_transformers.core',
 'tf_transformers.data',
 'tf_transformers.layers',
 'tf_transformers.layers.attention',
 'tf_transformers.layers.mask',
 'tf_transformers.layers.transformer',
 'tf_transformers.losses',
 'tf_transformers.models',
 'tf_transformers.models.model_configs',
 'tf_transformers.models.model_configs.albert',
 'tf_transformers.models.model_configs.bert',
 'tf_transformers.models.model_configs.gpt2',
 'tf_transformers.models.model_configs.mt5',
 'tf_transformers.models.model_configs.roberta',
 'tf_transformers.models.model_configs.t5',
 'tf_transformers.models.model_wrappers',
 'tf_transformers.text',
 'tf_transformers.utils',
 'tf_transformers.utils.convert']

package_data = \
{'': ['*'],
 'tf_transformers': ['notebooks/.ipynb_checkpoints/*',
                     'notebooks/conversion_scripts/*',
                     'notebooks/conversion_scripts/.ipynb_checkpoints/*',
                     'notebooks/experimental/*',
                     'notebooks/tensorflow_records/*',
                     'notebooks/tensorflow_records/.ipynb_checkpoints/*',
                     'notebooks/text_generation/*',
                     'notebooks/text_generation/.ipynb_checkpoints/*',
                     'notebooks/tutorials/*',
                     'notebooks/tutorials/.ipynb_checkpoints/*'],
 'tf_transformers.models.model_configs': ['unilm_cnndm/*']}

setup_kwargs = {
    'name': 'tf-transformers',
    'version': '0.1.0',
    'description': 'Simple Python project built with Poetry.',
    'long_description': '',
    'author': 'Sarath R Nair',
    'author_email': 's4sarath@gmail.com',
    'maintainer': 'Sarath R Nair',
    'maintainer_email': 's4sarath@gmail.com',
    'url': '',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
