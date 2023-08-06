# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vbnigmm',
 'vbnigmm.backend',
 'vbnigmm.backend.tensorflow',
 'vbnigmm.distributions',
 'vbnigmm.linalg',
 'vbnigmm.math',
 'vbnigmm.mixture']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19,<2.0',
 'scipy>=1.5,<2.0',
 'tensorflow>=2.4,<3.0',
 'tensorflow_probability>=0.12,<0.13']

setup_kwargs = {
    'name': 'vbnigmm',
    'version': '2.2.0',
    'description': 'Variational Bayes algorithm for normal inverse Gaussian mixture models',
    'long_description': 'vbnigmm\n=======\n\nVariational Bayes algorithm for Normal Inverse Gaussian Mixture Models\n\nDemonstration\n-------------\n\nThe results of the sample simulation data can be \nchecked by the following procedure:\n\n.. code-block:: bash\n\n    poetry run jupyter lab\n    # open example.ipynb in jupyter environment\n\nInstallation\n------------\n\nThe package can be build using poetry and installed using pip:\n\n.. code-block:: bash\n\n    poetry build\n    pip install dist/vbnigmm-2.0.0-py3-none-any.whl\n\nExamples\n--------\n\nIf you want to apply vbnigmm to your data,\nyou can run the following code:\n\n.. code-block:: python\n\n    from vbnigmm import NormalInverseGaussMixture as Model\n\n    # x is numpy.ndarray of 2D\n\n    model = Model()\n    model.fit(x)\n    label = model.predict(x)\n\nCitation\n--------\n\nIf you use vbnigmm in a scientific paper,\nplease consider citing the following paper:\n\nTakashi Takekawa, `Clustering of non-Gaussian data by variational Bayes for normal inverse Gaussian mixture models. <https://arxiv.org/abs/2009.06002>`_ arXiv preprint arXiv:2009.06002 (2020).\n',
    'author': 'TAKEKAWA Takashi',
    'author_email': 'takekawa@tk2lab.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tk2lab/vbnigmm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
