#############
Riskfolio-Lib
#############

.. meta::
   :description: Library for making quantitative strategic asset allocation or portfolio optimization in Python.
   :keywords: portfolio optimization python, portfolio optimization, Markowitz portfolio optimization, cvar portfolio optimization, asset allocation, strategic asset allocation


**Quantitative Strategic Asset Allocation, Easy for Everyone.**

.. image:: images/MSV_Frontier.png
    :width: 45%
    
.. image:: images/Pie_Chart.png
    :width: 45%

.. raw:: html

    <a href='https://ko-fi.com/B0B833SXD' target='_blank'><img height='36'style='border:0px;height:36px;' src='https://cdn.ko-fi.com/cdn/kofi1.png?v=2' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>


Description
===========

Riskfolio-Lib is a library for making quantitative strategic asset allocation
or portfolio optimization in Python made in Peru |:peru:|. It is built on top of
`CVXPY <https://www.cvxpy.org/>`_ and closely integrated
with `pandas <https://pandas.pydata.org/>`_ data structures.

Some of key functionalities that Riskfolio-Lib offers:

- Mean Risk Portfolio optimization with 4 objective functions:

    - Minimum Risk.
    - Maximum Return.
    - Maximum Utility Function.
    - Maximum Risk Adjusted Return Ratio.

- Mean Risk Portfolio optimization with 11 convex risk measures:

    - Standard Deviation.
    - Semi Standard Deviation.
    - Mean Absolute Deviation (MAD).
    - First Lower Partial Moment (Omega Ratio)
    - Second Lower Partial Moment (Sortino Ratio)
    - Conditional Value at Risk (CVaR).
    - Worst Case Realization (Minimax Model)
    - Maximum Drawdown (Calmar Ratio).
    - Average Drawdown
    - Conditional Drawdown at Risk (CDaR).
    - Ulcer Index.

- Risk Parity Portfolio optimization with 8 convex risk measures:

    - Standard Deviation.
    - Semi Standard Deviation.
    - Mean Absolute Deviation (MAD).
    - First Lower Partial Moment (Omega Ratio)
    - Second Lower Partial Moment (Sortino Ratio)
    - Conditional Value at Risk (CVaR).
    - Conditional Drawdown at Risk (CDaR).
    - Ulcer Index.

- Worst Case Mean Variance Portfolio optimization.
- Portfolio optimization with Black Litterman model.
- Portfolio optimization with Risk Factors model.
- Portfolio optimization with constraints on tracking error and turnover.
- Portfolio optimization with short positions and leveraged portfolios.
- Tools for build efficient frontier for 11 risk measures.
- Tools for build linear constraints on assets, asset classes and risk factors.
- Tools for build views on assets and asset classes.
- Tools for calculate risk measures.
- Tools for calculate risk contributions per asset.
- Tools for calculate uncertainty sets for mean vector and covariance matrix.
- Tools for estimate loadings matrix (Stepwise Regression and Principal Components Regression).
- Tools for visualizing portfolio properties and risk measures.


Contents
========

..  toctree::
    :maxdepth: 1

    Install <install>
    Portfolio Models <portfolio>
    Parameters Estimation <parameters>
    Constraints Functions <constraints>
    Risk Functions <risk>
    Plot Functions <plot>
    Auxiliary Functions <auxiliary>
    Examples <examples>
    Contributing <contributing>
    Authors <authors>
    License <license>
    Changelog <changelog>

    
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Module Plans
==================

The plan for this modules is to add more functions that will be very useful
to asset managers.

* Mean Entropic Risk Optimization Portfolios.
* Add functions to estimate Duration, Convexity, Key Rate Durations and Convexities of bonds without embedded options (for loadings matrix).
* Add more functions based on suggestion of users.
