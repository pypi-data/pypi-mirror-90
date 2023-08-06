# History

## 0.4.0 - 2020-12-30

This release increases the supported version of python to 3.8 and also includes changes in the
installation requirements, where ``pandas`` and ``scikit-optimize`` packages have been updated
to support higher versions.

## Internal improvements

* Added github actions.

### Resolved Issues

* Issue #210: Integrate Scikit-Optimize for benchmarking.

## 0.3.12 - 2020-09-08

In this release BTB includes two new tuners, `GCP` and `GCPEi`. which use a
`GaussianProcessRegressor` meta-model from `sklearn.gaussian_process` applying
`copulas.univariate.Univariate` transformations to the input data and afterwards reverts it for
the predictions.

### Resolved Issues

* Issue #15: Implement a `GaussianCopulaProcessRegressor`.
* Issue #205: Separate datasets from `MLChallenge`.
* Issue #208: Implement `GaussianCopulaProcessMetaModel`.

## 0.3.11 - 2020-06-12

With this release we fix the `AX.optimize` tuning function by casting the values of the
hyperparameters to the type of value that they represent.

### Resolved Issues

* Issue #201: Fix AX.optimize malfunction.

## 0.3.10 - 2020-05-29

With this release we integrate a new tuning library, `SMAC`, with our benchmarking process. A new
leaderboard including this library has been generated. The following two tuners from this library
have been added:
* `SMAC4HPO`: Bayesian optimization using a Random Forest model of *pyrfr*.
* `HB4AC`: Uses Successive Halving for proposals.

### Internal improvements

* Renamed `btb_benchmark/tuners` to `btb_benchmark/tuning_functions`.
* Ready to use tuning functions from `btb_benchmark/tuning_functions`.

### Resolved Issues

* Issue #195: Integrate `SMAC` for benchmarking.

## 0.3.9 - 2020-05-18

With this release we integrate a new tuning library, `Ax`, with our benchmarking process. A new
leaderboard including this library has been generated.

### Resolved Issues

* Issue #194: Integrate `Ax` for benchmarking.

## 0.3.8 - 2020-05-08

This version adds a new functionality which allows running the benchmarking framework on a
Kubernetes cluster. By doing this, the benchmarking process can be executed distributedly, which
reduces the time necessary to generate a new leaderboard.

### Internal improvements

* `btb_benchmark.kubernetes.run_dask_function`: Run dask function inside a pod using the given
config.
* `btb_benchmark.kubernetes.run_on_kubernetes`: Start a Dask Cluster using dask-kubernetes and
run a function.
* Documentation updated.
* Jupyter notebooks with examples on how to run the benchmarking process and how to run it on
kubernetes.

## 0.3.7 - 2020-04-15

This release brings a new `benchmark` framework with public leaderboard.
As part of our benchmarking efforts we will run the framework at every release and make the results
public. In each run we compare it to other tuners and optimizer libraries. We are constantly adding
new libraries for comparison. If you have suggestions for a tuner library we should include in our
compraison, please contact us via email at [dailabmit@gmail.com](mailto:dailabmit@gmail.com).

### Resolved Issues

* Issue #159: Implement more `MLChallenges` and generate a public leaderboard.
* Issue #180: Update BTB Benchmarking module.
* Issue #182: Integrate HyperOPT with benchmarking.
* Issue #184: Integrate dask to bencharking.

## 0.3.6 - 2020-03-04

This release improves `BTBSession` error handling and allows `Tunables` with cardinality
equal to 1 to be scored with `BTBSession`. Also, we provide a new documentation for
this version of `BTB`.

### Internal Improvements

Improved documentation, unittests and integration tests.

### Resolved Issues

* Issue #164: Improve documentation for `v0.3.5+`.
* Issue #166: Wrong erro raised by BTBSession on too many errors.
* Issue #170: Tuner has no scores attribute until record is run once.
* Issue #175: BTBSession crashes when record is not performed.
* Issue #176: BTBSession fails to select a proper Tunable when normalized_scores becomse None.

## 0.3.5 - 2020-01-21

With this release we are improving `BTBSession` by adding private attributes, or not intended to
be public / modified by the user and also improving the documentation of it.

### Internal Improvements

Improved docstrings, unittests and public interface of `BTBSession`.

### Resolved Issues

* Issue #162: Fix session with the given comments on PR 156.

## 0.3.4 - 2019-12-24

With this release we introduce a `BTBSession` class. This class represents the process of selecting
and tuning several tunables until the best possible configuration fo a specific `scorer` is found.
We also have improved and fixed some minor bugs arround the code (described in the issues below).

### New Features

* `BTBSession` that makes `BTB` more user friendly.

### Internal Improvements

Improved unittests, removed old dependencies, added more `MLChallenges` and fixed an issue with
the bound methods.

### Resolved Issues

* Issue #145: Implement `BTBSession`.
* Issue #155: Set defaut to `None` for `CategoricalHyperParam` is not possible.
* Issue #157: Metamodel `_MODEL_KWARGS_DEFAULT` becomes mutable.
* Issue #158: Remove `mock` dependency from the package.
* Issue #160: Add more Machine Learning Challenges and more estimators.


## 0.3.3 - 2019-12-11

Fix a bug where creating an instance of `Tuner` ends in an error.

### Internal Improvements

Improve unittests to use `spec_set` in order to detect errors while mocking an object.

### Resolved Issues

* Issue #153: Bug with tunner logger message that avoids creating the Tunner.

## 0.3.2 - 2019-12-10

With this release we add the new `benchmark` challenge `MLChallenge` which allows users to
perform benchmarking over datasets with machine learning estimators, and also some new
features to make the workflow easier.

### New Features

* New `MLChallenge` challenge that allows performing crossvalidation over datasets and machine
learning estimators.
* New `from_dict` function for `Tunable` class in order to instantiate from a dictionary that
contains information over hyperparameters.
* New `default` value for each hyperparameter type.

### Resolved Issues

* Issue #68: Remove `btb.tuning.constants` module.
* Issue #120: Tuner repr not helpful.
* Issue #121: HyperParameter repr not helpful.
* Issue #141: Imlement propper logging to the tuning section.
* Issue #150: Implement Tunable `from_dict`.
* Issue #151: Add default value for hyperparameters.
* Issue #152: Support `None` as a choice in `CategoricalHyperPrameters`.

## 0.3.1 - 2019-11-25

With this release we introduce a `benchmark` module for `BTB` which allows the users to perform
a benchmark over a series of `challenges`.

### New Features

* New `benchmark` module.
* New submodule named `challenges` to work toghether with `benchmark` module.

### Resolved Issues

* Issue #139: Implement a Benchmark for BTB

## 0.3.0 - 2019-11-11

With this release we introduce an improved `BTB` that has a major reorganization of the project
with emphasis on an easier way of interacting with `BTB` and an easy way of developing, testing and
contributing new acquisition functions, metamodels, tuners  and hyperparameters.

### New project structure

The new major reorganization comes with the `btb.tuning` module. This module provides everything
needed for the `tuning` process and comes with three new additions `Acquisition`, `Metamodel` and
`Tunable`. Also there is an update to the `Hyperparamters` and `Tuners`. This changes are meant
to help developers and contributors to easily develop, test and contribute new `Tuners`.

### New API

There is a slightly new way of using `BTB` as the new `Tunable` class is introduced, that is meant
to be the only requiered object to instantiate a `Tuner`. This `Tunable` class represents a
collection of `HyperParams` that need to be tuned as a whole, at once. Now, in order to create a
`Tuner`, a `Tunable` instance must be created first with the `hyperparameters` of the
`objective function`.

### New Features

* New `Hyperparameters` that allow an easier interaction for the final user.
* New `Tunable` class that manages a collection of `Hyperparameters`.
* New `Tuner` class that is a python mixin that requieres of `Acquisition` and `Metamodel` as
parents. Also now works with a single `Tunable` object.
* New `Acquisition` class, meant to implement an acquisition function to be inherit by a `Tuner`.
* New `Metamodel` class, meant to implement everything that a certain `model` needs and be inherit
by the `Tuner`.
* Reorganization of the `selection` module to follow a similar `API` to `tuning`.

### Resolved Issues

* Issue #131: Reorganize the project structure.
* Issue #133: Implement Tunable class to control a list of hyperparameters.
* Issue #134: Implementation of Tuners for the new structure.
* Issue #140: Reorganize selectors.

## 0.2.5

### Bug Fixes

* Issue #115: HyperParameter subclass instantiation not working properly

## 0.2.4

### Internal Improvements

* Issue #62: Test for `None` in `HyperParameter.cast` instead of `HyperParameter.__init__`

### Bug fixes

* Issue #98: Categorical hyperparameters do not support `None` as input
* Issue #89: Fix the computation of `avg_rewards` in `BestKReward`

## 0.2.3

### Bug Fixes

* Issue #84: Error in GP tuning when only one parameter is present bug
* Issue #96: Fix pickling of HyperParameters
* Issue #98: Fix implementation of the GPEi tuner

## 0.2.2

### Internal Improvements

* Updated documentation

### Bug Fixes

* Issue #94: Fix unicode `param_type` caused error on python 2.

## 0.2.1

### Bug fixes

* Issue #74: `ParamTypes.STRING` tunables do not work

## 0.2.0

### New Features

* New Recommendation module
* New HyperParameter types
* Improved documentation and examples
* Fully tested Python 2.7, 3.4, 3.5 and 3.6 compatibility
* HyperParameter copy and deepcopy support
* Replace print statements with logging

### Internal Improvements

* Integrated with Travis-CI
* Exhaustive unit testing
* New implementation of HyperParameter
* Tuner builds a grid of real values instead of indices
* Resolve Issue #29: Make args explicit in `__init__` methods
* Resolve Issue #34: make all imports explicit

### Bug Fixes

* Fix error from mixing string/numerical hyperparameters
* Inverse transform for categorical hyperparameter returns single item

## 0.1.2

* Issue #47: Add missing requirements in v0.1.1 setup.py
* Issue #46: Error on v0.1.1: 'GP' object has no attribute 'X'

## 0.1.1

* First release.
