## Overview

This meta package will install the python packages that together make up the `methylsuite`:

- `methylprep` is a python package for processing DNA methylation data from Illumina arrays. It provides:
    - A variety of background subtraction and normalization methods found in similar R-based packages.
    - Support for Illumina arrays (27k, 450k, EPIC, mouse).
    - Support for analyzing public data sets from GEO (the NIH Gene Expression Omnibus is a database) .
    - Support for managing data in `Pandas` DataFrames.
- `methylcheck` includes:
   - quality control (QC) functions for filtering out unreliable probes, based on the published literature,  sample outlier detection, plots similar to Genome Studio functions, sex prediction, and
   and interactive method for assigning samples to groups, based on array data, in a Jupyter notebook.
- `methylize` provides these analysis functions:
   - differentially methylated probe statistics (between treatment and control samples).
   - volcano plots (which probes are the most different).
   - manhattan plot (where in genome are the differences).

### Parts of `methylsuite`
![](https://github.com/FOXOBioScience/methylprep/blob/master/docs/methyl-suite.png?raw=true)

### Data Processing
![processing pipeline](https://github.com/FOXOBioScience/methylprep/blob/master/docs/methylprep-processing-pipeline.png?raw=true)

### Quality Control
![methylcheck pipeline](https://raw.githubusercontent.com/FOXOBioScience/methylcheck/master/docs/methylcheck_functions.png)

## Installation

This all-in-one command will install all three packages and their required dependencies.

```python
pip3 install methylsuite
```

This command was tested in a naive minimal conda environment, created thusly:

```python
conda create -n testsuite
```

Afterwards, I had to install `statsmodels` using conda apart from the other dependencies, like so:

```python
conda install statsmodels
pip3 install methylsuite
```

(Statsmodels uses additional C-compilers during installation)
