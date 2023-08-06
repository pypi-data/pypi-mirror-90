# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lipo']

package_data = \
{'': ['*']}

install_requires = \
['dlib>=19.21.1,<20.0.0', 'scikit-learn>=0.22.1', 'tqdm>=4.55.0,<5.0.0']

extras_require = \
{'github-actions': ['pytest-github-actions-annotate-failures']}

setup_kwargs = {
    'name': 'lipo',
    'version': '1.2.2',
    'description': 'Global, derivative- and parameter-free (hyperparameter) optimization',
    'long_description': 'LIPO is a package for derivative- and parameter-free global optimization, e.g.\nfor hyperparameter tuning. Is based on\nthe `dlib` package and provides wrappers around its optimization routine.\n\nThe algorithm outperforms random search - sometimes by margins as large as 10000x. It is often preferable to\nBayesian optimization which requires "tuning of the tuner". Performance is on par with moderately to well tuned Bayesian\noptimization.\n\nThe provided implementation has the option to automatically enlarge the search space if bounds are found to be\ntoo restrictive (i.e. the optimum being to close to one of them).\n\nSee the [LIPO algorithm implementation](http://dlib.net/python/index.html#dlib.find_max_global) for details.\n\nA [great blog post](http://blog.dlib.net/2017/12/a-global-optimization-algorithm-worth.html) by the author of\n`dlib` exists, describing how it works.\n\n# Installation\n\nExecute\n\n`pip install lipo`\n\n# Usage\n\n```python\nfrom lipo import GlobalOptimizer\n\ndef function(x, y, z):\n    zdict = {"a": 1, "b": 2}\n    return -((x - 1.23) ** 6) + -((y - 0.3) ** 4) * zdict[z]\n\npre_eval_x = dict(x=2.3, y=13, z="b")\nevaluations = [(pre_eval_x, function(**pre_eval_x))]\n\nsearch = GlobalOptimizer(\n    function,\n    lower_bounds={"x": -10.0, "y": -10},\n    upper_bounds={"x": 10.0, "y": -3},\n    categories={"z": ["a", "b"]},\n    evaluations=evaluations,\n    maximize=True,\n)\n\nnum_function_calls = 1000\nsearch.run(num_function_calls)\n```\n\nThe optimizer will automatically extend the search bounds if necessary.\n\nFurther, the package provides an implementation of the scikit-learn interface for\nhyperparamter search.\n\n```python\nfrom lipo import LIPOSearchCV\n\nsearch = LIPOSearchCV(\n    estimator,\n    param_space={"param_1": [0.1, 100], "param_2": ["category_1", "category_2"]},\n    n_iter=100\n)\nsearch.fit(X, y)\nprint(search.best_params_)\n```\n\n# Comparison to other frameworks\n\nFor benchmarks, see the notebook in the `benchmark` directory.\n\n## [scikit-optimize](https://scikit-optimize.github.io/)\n\nThis is a Bayesian framework.\n\n`+` A well-chosen prior can lead to very good results slightly faster\n\n`-` If the wrong prior is chosen, tuning can take long\n\n`-` It is not parameter-free - one can get stuck in a local minimum which means tuning of the tuner can be required\n\n`-` LIPO can converge faster when it is close to the minimum using a quadratic approximation\n\n`-` The exploration of the search space is not systematic, i.e. results can vary a lot from run to run\n\n## [Optuna](https://optuna.readthedocs.io/)\n\n`+` It parallelizes very well\n\n`+` It can stop training early. This is very useful, e.g. for neural networks and can speed up tuning\n\n`+` A well-chosen prior can lead to very good results slightly faster\n\n`-` If the wrong prior is chosen, tuning can take long\n\n`-` It is not parameter-free, i.e. some tuning of the tuner can be required (the defaults are pretty good though)\n\n`-` LIPO can converge faster when it is close to the minimum using a quadratic approximation\n\n`-` The exploration of the search space is not systematic, i.e. results can vary a lot from run to run\n',
    'author': 'Jan Beitner',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jdb78/lipo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
