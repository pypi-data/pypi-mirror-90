==================================
Bayesian estimation of proportions
==================================

.. image:: https://img.shields.io/pypi/v/bayespropestimation.svg
        :target: https://pypi.python.org/pypi/bayespropestimation




Simple class and methods for the Bayesian estimation and comparison of proportions.

* Free software: MIT license

Features
--------

* Estimates the posterior distribution of the mean parameter for two binomial samples, A and B.
* Estimates the posterior distribution of the difference in mean parameters for two binomial samples, A and B.
* Provides summary statistics and visualisations for the estimated parameters.
* The prior distribution, sample count, random seed, credible intervals and parameter names can all be customised.

Need to work with continuous data?
-----------------------------------

See the `bayestestimation <https://github.com/oli-chipperfield/bayestestimation>`_ module for a counterpart to this module.  Designed for working with continuous data.


============
Installation
============

Stable release
--------------

To install Bayesian estimation of proportions, run this command in your terminal:

.. code-block:: console

    $ pip install bayespropestimation

This is the preferred method to install the module, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/

From sources
------------

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/oli-chipperfield/bayespropestimation

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/oli-chipperfield/bayespropestimation/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install

.. _Github repo: https://github.com/oli-chipperfield/bayespropestimation
.. _tarball: https://github.com/oli-chipperfield/bayespropestimation/tarball/master

===========
Methodology
===========

See `notebook <https://github.com/oli-chipperfield/bayespropestimation/blob/master/docs/bayespropestimation_basis.ipynb>`_ for details.

=====
Usage
=====

To use Bayesian estimation of proportions in a project

.. code-block:: python

    import bayespropestimation

Simple example
--------------

To carry out a simple estimation of the posterior density of two samples and an estimate of the difference, using an uninformative prior.  Import the ``BayesProportionsEstimation`` class.

.. code-block:: python

    from bayespropestimation.bayespropestimation import BayesProportionsEstimation

Define data from samples A and B as two lists in the format ``[successes, trials]`` and initialise the ``BayesProportionsEstimation`` class.

.. code-block:: python

    a = [10, 50]
    b = [20, 50]
    ExampleBayes = BayesProportionsEstimation(a, b)

Posterior densities are estimated when the class is intialised. There are five methods for accessing information about the draws from simulations of the posterior densities.

.. code-block:: python

    ExampleBayes.get_posteriors()
    # Returns tuple of samples from the posterior distributions of parameters

.. code-block:: python

    ExampleBayes.hdi_summary()
    # Returns dataframe of the high-density-interval (HDI), maximum-a-posteriori (MAP) and mean of samples from the posteriores

.. image:: https://github.com/oli-chipperfield/bayespropestimation/blob/master/images/example_hdi.png

.. code-block:: python

    ExampleBayes.quantile_summary()
    # Returns dataframe of quantiles and mean of the posterior densities of samples for parameters

.. image:: https://github.com/oli-chipperfield/bayespropestimation/blob/master/images/example_quantile.png

.. code-block:: python

    ExampleBayes.infer_delta_probability()
    # Returns probability estimate of the delta parameter being greater than 0, plus an aid to inference.  
    # Includes an optional print out of the probability and inference.
    
    'The probability that theta_b is greater than theta_a is 98.63%. Therefore theta_b is almost certainly greater than theta_a.'
    '(0.9863, 'almost certainly')'

.. code-block:: python

    ExampleBayes.infer_delta_bayes_factor()
    # Returns the Bayes factor of the hypothesis that P(theta_b > theta_a | D) where D is the data, plus an aid to inference.  
    # Includes an optional print out of the Bayes factor and inference.

    'The calculated bayes factor for the hypothesis that theta_b is greater than theta_a versus the hypothesis that theta_a is greater than theta_a is 71.993. Therefore the strength of evidence for this hypothesis is very strong.'
    '(71.99270072992677, 'very strong')'

.. code-block:: python

    ExampleBayes.posterior_plot
    # Returns KDE plots of samples from the posterior densities of the parameters

.. image:: https://github.com/oli-chipperfield/bayespropestimation/blob/master/images/example_posterior_plot.png

To see how to use non-default parameters refer to the `usage guide <https://github.com/oli-chipperfield/bayespropestimation/blob/master/docs/bayespropestimation_usage.ipynb>`_ or refer to the doc-strings in the `source <https://github.com/oli-chipperfield/bayespropestimation/bayespropestimation/bayespropestimation.py>`_.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

.. highlight:: shell
