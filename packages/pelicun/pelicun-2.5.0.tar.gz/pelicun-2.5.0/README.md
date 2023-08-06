<p align="center">
	<img src="https://raw.githubusercontent.com/NHERI-SimCenter/pelicun/master/doc_src/common/figures/pelicun-Logo-white.png" 
		alt="pelicun" align="middle" height="200"/>
</p>

<p align="center">
	<a href="https://travis-ci.org/NHERI-SimCenter/pelicun", alt="TravisCI">
		<img src="https://travis-ci.org/NHERI-SimCenter/pelicun.svg?branch=master" /></a>
	<a href="https://coveralls.io/github/NHERI-SimCenter/pelicun?branch=master", alt="Coverage Status">
		<img src="https://coveralls.io/repos/github/NHERI-SimCenter/pelicun/badge.svg?branch=master" /></a>
</p>

<p align="center">
	<a href="https://doi.org/10.5281/zenodo.2558558", alt="DOI">
		<img src="https://zenodo.org/badge/DOI/10.5281/zenodo.2558558.svg" /></a>
</p>

<p align="center">
	<b>Probabilistic Estimation of Losses, Injuries, and Community resilience Under Natural disasters</b>
</p>

## What is it?

`pelicun` is a Python package that provides tools for assessment of damage and losses due to natural hazards. It uses a stochastic damage and loss model that is based on the methodology described in FEMA P58 (FEMA, 2012). While FEMA P58 aims to assess the seismic performance of a building, with `pelicun` we provide a more versatile, hazard-agnostic tool that estimates losses for several types of assets in the built environment.

Detailed documentation of the available methods and their use is available at http://nheri-simcenter.github.io/pelicun

## What can I use it for?

`pelicun` quantifies losses from an earthquake or hurricane scenario in the form of decision variables. This functionality is typically utilized for performance-based engineering and regional risk assessment. There are several steps of performance assessment that `pelicun` can help with:

- **Describe the joint distribution of asset response.** The response of a structure or other type of asset to an earthquake or hurricane wind is typically described by so-called engineering demand parameters (EDPs). `pelicun` provides methods that take a finite number of EDP vectors and find a multivariate distribution that describes the joint distribution of EDP data well. You can control the type of target distribution, apply truncation limits and censor part of the data to consider detection limits in your analysis. Alternatively, you can choose to use your EDP vectors as-is without resampling from a fitted distribution.

- **Define the damage and loss model of a building.** The component damage and loss data from the first two editions of FEMA P58 and the HAZUS earthquake and hurricane models for buildings are provided with pelicun. This makes it easy to define building components without having to collect and provide all the data manually. The stochastic damage and loss model is designed to facilitate modeling correlations between several parameters of the damage and loss model.

- **Estimate component damages.** Given a damage and loss model and the joint distribution of EDPs, `pelicun` provides methods to estimate the amount of damaged components and the number of cases with collapse.

- **Estimate consequences.** Using information about collapse and component damages, the following consequences can be estimated with the loss model: reconstruction cost and time, unsafe placarding (red tag), injuries and fatalities. 

## Why should I use it?

1. It is free and it always will be. 
2. It is open source. You can always see what is happening under the hood.
3. It is efficient. The loss assessment calculations in `pelicun` use `numpy`, `scipy`, and `pandas` libraries to efficiently propagate uncertainties and provide detailed results quickly.
4. You can trust it. Every function in `pelicun` is tested after every commit. See the Travis-CI and Coveralls badges at the top for more info. 
5. You can extend it. If you have other methods that you consider better than the ones we already offer, we encourage you to fork the repo, and extend `pelicun` with your approach. You do not need to share your extended version with the community, but if you are interested in doing so, contact us and we are more than happy to merge your version with the official release.

## Requirements

`pelicun` runs under Python 3.6+ . The following packages are required for it to work properly:

- `numpy` >= 1.19.0

- `scipy` >= 1.5.0

- `pandas` >= 1.1.0

We recommend installing these using `pip`.

## Installation

`pelicun` is available at the Python Package Index (PyPI). You can simply install it using `pip` as follows:

```
pip install pelicun
```

## Changelog

### Major changes in v2.5

* Extend the uq module to support:
    * More efficient sampling, especially when most of the random variables in the model are either independent or perfectly correlated.
    * More accurate and more efficient fitting of multivariate probability distributions to raw EDP data.
    * Arbitrary marginals (i.e., beyond the basic Normal and Lognormal) for joint distributions.
    * Latin Hypercube Sampling
* Aggregate DL data from JSON files to HDF5 files to reduce the number of files and make it easier to share databases.
* Add log file that records every important calculation detail and warnings.
* Extend auto-population logic with solutions for HAZUS EQ assessments. 
* Introduce external auto-population scripts and provide an example for hurricane assessments.
* Add a script to help users convert HDF files to CSV (HDF_to_CSV.py under tools)
* Use unique and standardized attribute names in the input files
* Add new EDP types: RID, PMD, SA, SV, SD, PGD, DWD, RDR.
* Migrate to the latest version of Python, numpy, scipy, and pandas see setup.py for required minimum versions of those tools.
* Bug fixes and minor improvements to support user needs:
    * Add 1.2 scale factor for EDPs controlling non-directional Fragility Groups.
    * Remove dependency on scipy's truncnorm function to avoid long computation times due to a bug in recent scipy versions.

## License

`pelicun` is distributed under the BSD 3-Clause license, see LICENSE.

## Acknowledgement

This material is based upon work supported by the National Science Foundation under Grant No. 1612843. Any opinions, findings, and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the National Science Foundation.

## Contact

Adam Zsarnóczay, NHERI SimCenter, Stanford University, adamzs@stanford.edu
