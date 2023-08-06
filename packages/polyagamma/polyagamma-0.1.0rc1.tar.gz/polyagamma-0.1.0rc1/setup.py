# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['__init__']
install_requires = \
['numpy>=1.17.0,<2.0.0']

setup_kwargs = {
    'name': 'polyagamma',
    'version': '0.1.0rc1',
    'description': "Efficiently sample from the Polya-Gamma distribution using NumPy's Generator interface",
    'long_description': '# polya-gamma\nEfficiently sample from the Polya-Gamma distribution using NumPy\'s Generator interface.\n\n\n## Dependencies\n- Numpy >= 1.17 \n\n\n## Installation\n```shell\n$ pip install -U polyagamma\n```\n\n\n## Example\n\n### Python\n\n`polyagamma` can act as a drop-in replacement for numpy\'s Generator class.\n```python\nimport numpy as np\n\nfrom polyagamma import default_rng, Generator\n\ng = Generator(np.random.PCG64())  # or use default_rng()\nprint(g.polyagamma())\n\n# Get a 5 by 10 array of PG(1, 2) variates.\nprint(g.polyagamma(z=2, size=(5, 10)))\n\n# Pass sequences as input. Numpy\'s broadcasting semantics apply here.\nh = [[1, 2, 3, 4, 5], [9, 8, 7, 6, 5]]\nprint(g.polyagamma(h, 1))\n\n# Pass an output array\nout = np.empty(5)\ng.polyagamma(out=out)\nprint(out)\n\n# one can choose a sampling method from {devroye, alternate, gamma}.\n# If not given, the default behaviour is a hybrid sampler that picks\n# the best method based on the parameter values\nout = g.polyagamma(method="devroye")\n\n# other numpy distributions are still accessible\nprint(g.standard_normal())\nprint(g.standard_gamma())\n```\n### C\nFor an example of how to use `polyagamma` in a C program, see [here][1].\n\n## TODO\n- ~~Add devroye and gamma convolution methods.~~\n- ~~Add the "alternate" sampling method.~~\n- ~~Add the hybrid sampler based on a combination of available methods.~~\n- Add the "saddle point approximation" method.\n- Add the hybrid sampler based on all four methods.\n- ~~Add array broadcasting support for paramater inputs.~~\n\n\n## References\n- Luc Devroye. "On exact simulation algorithms for some distributions related to Jacobi theta functions." Statistics & Probability Letters, Volume 79, Issue 21, (2009): 2251-2259.\n- Polson, Nicholas G., James G. Scott, and Jesse Windle. "Bayesian inference for logistic models using Pólya–Gamma latent variables." Journal of the American statistical Association 108.504 (2013): 1339-1349.\n- J. Windle, N. G. Polson, and J. G. Scott. "Improved Polya-gamma sampling". Technical Report, University of Texas at Austin, 2013b.\n- Windle, Jesse, Nicholas G. Polson, and James G. Scott. "Sampling Polya-Gamma random variates: alternate and approximate techniques." arXiv preprint arXiv:1405.0506 (2014)\n\n\n[1]: https://github.com/zoj613/htnorm/blob/main/examples/c_polyagamma.c\n',
    'author': 'Zolisa Bleki',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zoj613/polya-gamma/',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
