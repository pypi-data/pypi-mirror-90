# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['vbnigmm',
 'vbnigmm.backend',
 'vbnigmm.backend.tensorflow',
 'vbnigmm.distributions',
 'vbnigmm.linalg',
 'vbnigmm.mixture']

package_data = \
{'': ['*']}

install_requires = \
['tensorflow>=2.4,<3.0']

setup_kwargs = {
    'name': 'vbnigmm',
    'version': '2.3.1',
    'description': 'Variational Bayes algorithm for normal inverse Gaussian mixture models',
    'long_description': 'vbnigmm\n=======\n\nVariational Bayes algorithm for Normal Inverse Gaussian Mixture Models\n\nInstallation\n------------\n\nThe package can be build using poetry and installed using pip:\n\n.. code-block:: bash\n\n    pip install vbnigmm\n\nExamples\n--------\n\nIf you want to apply vbnigmm to your data,\nyou can run the following code:\n\n.. code-block:: python\n\n    from vbnigmm import NormalInverseGaussMixture as Model\n\n    # x is numpy.ndarray of 2D\n\n    model = Model()\n    model.fit(x)\n    label = model.predict(x)\n\nCitation\n--------\n\nIf you use vbnigmm in a scientific paper,\nplease consider citing the following paper:\n\nTakashi Takekawa, `Clustering of non-Gaussian data by variational Bayes for normal inverse Gaussian mixture models. <https://arxiv.org/abs/2009.06002>`_ arXiv preprint arXiv:2009.06002 (2020).\n',
    'author': 'TAKEKAWA Takashi',
    'author_email': 'takekawa@tk2lab.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tk2lab/vbnigmm',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
