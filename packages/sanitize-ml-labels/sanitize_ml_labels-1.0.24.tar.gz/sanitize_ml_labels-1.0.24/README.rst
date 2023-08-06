sanitize_ml_labels
=========================================================================================
|travis| |sonar_quality| |sonar_maintainability| |pip| |downloads|

Simple python package to sanitize in a standard way ML-related labels.

How do I install this package?
----------------------------------------------
As usual, just download it using pip:

.. code:: shell

    pip install sanitize_ml_labels

Tests Coverage
----------------------------------------------
Since some software handling coverages sometime get slightly different results, here's two of them:

|coveralls| |sonar_coverage|

Why do I need this?
-------------------
So you have some kind of plot and you have some ML-related labels.
Since I always rename and sanitize them the same way, I have prepared
this package to always sanitize them in a standard fashion.

Usage examples
----------------------------------------------
Here you have a couple of common examples: you have a set of metrics to normalize or a set of model names to normalize.

.. code:: python

    from sanitize_ml_labels import sanitize_ml_labels

    # Example for metrics
    labels = [
        "acc",
        "loss",
        "auroc",
        "lr"
    ]

    sanitize_ml_labels(labels)

    # ["Accuracy", "Loss", "AUROC", "Learning rate"]

    # Example for models
    labels = [
        "vanilla mlp",
        "vanilla cnn",
        "vanilla ffnn",
        "vanilla perceptron"
    ]

    sanitize_ml_labels(labels)

    # ["MLP", "CNN", "FFNN", "Perceptron"]


Extra utilities
---------------
Since I always use metric sanitization alongside axis normalization, it is useful to know which axis
should be maxed between zero and one to avoid any visualization bias to the metrics.

For this reason I have created the method :code:`is_normalized_metric`, which after having normalized the given metric
validates it against known normalized metrics (metrics between 0 and 1, is there another name? I could not figure out a better one).

.. code:: python

    from sanitize_ml_labels import is_normalized_metric

    is_normalized_metric("MSE") # False
    is_normalized_metric("acc") # True
    is_normalized_metric("accuracy") # True
    is_normalized_metric("AUROC") # True
    is_normalized_metric("auprc") # True


New features and issues
-----------------------
As always, for new features and issues you can either open a new issue and pull request.
A pull request will always be the quicker way, but I'll look into the issues when I get the time.

.. |travis| image:: https://travis-ci.org/LucaCappelletti94/sanitize_ml_labels.png
   :target: https://travis-ci.org/LucaCappelletti94/sanitize_ml_labels
   :alt: Travis CI build

.. |sonar_quality| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_sanitize_ml_labels&metric=alert_status
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_sanitize_ml_labels
    :alt: SonarCloud Quality

.. |sonar_maintainability| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_sanitize_ml_labels&metric=sqale_rating
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_sanitize_ml_labels
    :alt: SonarCloud Maintainability

.. |sonar_coverage| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_sanitize_ml_labels&metric=coverage
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_sanitize_ml_labels
    :alt: SonarCloud Coverage

.. |coveralls| image:: https://coveralls.io/repos/github/LucaCappelletti94/sanitize_ml_labels/badge.svg?branch=master
    :target: https://coveralls.io/github/LucaCappelletti94/sanitize_ml_labels?branch=master
    :alt: Coveralls Coverage

.. |pip| image:: https://badge.fury.io/py/sanitize-ml-labels.svg
    :target: https://badge.fury.io/py/sanitize-ml-labels
    :alt: Pypi project

.. |downloads| image:: https://pepy.tech/badge/sanitize-ml-labels
    :target: https://pepy.tech/badge/sanitize-ml-labels
    :alt: Pypi total project downloads 