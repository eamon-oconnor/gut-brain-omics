# Project Title

gut-brain-omics

## Description

The program gut-brain-omics.py takes one or more pairs of disease phenotype and bacteria species/genus in the gut microbiome and performs a set of tests to determine a correlation. Analyses include a Mann-Whitney U test and Welch's t-test for relative abundance of the given bacteria in the gut microbiome between the disease group and a healthy control group. Histograms and QQ plots for the two datasets are generated as well. Finally, mean relative abundance and standard deviation of the specified bacteria is calculated for both the disease and health group. By default the data is transformed using a box-cox transformation for each test and plot except the Mann-Whitney U test, however this option can be disabled or a different transformation can be used.

The main script includes functions to process inputs. It also imports functions from the query and utils modules. The query module includes functions meant to query information and data from API's including the MeSH RDF API, Ensembl REST API, and GMrepo RESTful API. The utils module includes functions to perform analyses of data including normality transformations, basic statistics, and histogram plotting.

Given phenotype/bacteria pairs must exist in the GMrepo database for analyses to be performed.

## Getting Started

### Dependencies

The project was written on the Ubuntu Linux opersating system on Python 3.10.12. It uses the argparse, pandas, scipy, statsmodels, pylab, sys, numpy, statistics, matplotlib, json, requests, and sys libraries.

### Installing

The program files can be cloned from github: "https://github.com/eamon-oconnor/gut-brain-omics"

### Executing program

The program gut-brain-omics.py can be run from the command line with the following format:
```
python3 gut-brain-omics.py --infile "file_path.csv" --phenotype "Phenotype name/id" --genus "Genus/species name/id" --outdir "result_directory" --transformation "transformation type" --alternative "test alternative"
```
Accepted disease phenotypes and bacteria genera/species are available to view on the GMrepo database. For phenotypes, the name as it appears on the GMrepo database can be entered, or the associated MeSH ID can be entered. For genera/species, the scientific name or NCBI ID can be entered.

The infile option allows users to input a CSV with phenotype/genus pairs. An input CSV must include a column labelled "Phenotype" and a column labelled "Genus". Alternatively, users can use the pphenotype and genus options to specify a single pair from the command line. The infile, phenotype, and genus options are thus optional however the script will terminate if at least one valid phenotype/genus pair is not given.

The outdir option is required and specifies an output directory to save generated plots to.

Accepted data transformations include "boxcox", "log10", "ln", and "None". This argument is optional and a boxcox transformation will be applied by default.

Accepted alternatives include "two-sided", "greater" (disease mean relative abundance greater than health), and "less" (disease mean relative abundance lesser than health). The specified alternative is used as the alternative hypothesis for both the Mann-Whitney U test and Welch's t-test. This argument is optional and a two-sided test will be used by default.

An example of a command line input and output for the program would be:
```
python3 gut-brain-omics.py --phenotype Depression --genus Bifidobacterium --outdir results

The mean relative abundance of Bifidobacterium in the Depression group is 1.145, with a standard deviation of 2.608.
The mean relative abundance of Bifidobacterium in the health group is 8.001, with a standard deviation of 16.985.
A Welch's t-test of Bifidobacterium abundance between the Depression group and healthy group produced a p-value of 2.044e-48.
A Mann-Whitney U test of Bifidobacterium abundance between the Depression group and healthy group produced a p-value of 3.292e-42.
```

## Help

An error will be returned if the module utils.py or query.py is not found within the relative directory modules/ with __init__.py present in the same directory. An error will also be returned if a given phenotype is not present in the MeSH database, a given genus/species is not present in the NCBI database, or data for a given phenotype/genus pair does not exist in the GMrepo database. After the error is printed, the script will continue to process any other input pairs.

The following error commonly occurs when running the script on a Windows OS:

```
qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.

Available platform plugins are: linuxfb, minimal, offscreen, vnc, webgl, xcb.
```

This error can be fixed by running one of the two following lines:

```
sudo apt install libxcb-xinerama0
export QT_QPA_PLATFORM=offscreen
```

The following command line input can be run for more information on the arguments and usage of the program gut-brain-omics.py:
```
python3 gut-brain-omics.py -h
```

The help() command can be run for information on the arguments, parameters, and return of the programs functions.

The following command line inputs can be run for more information on the project modules:

```
python3 -m pydoc modules/utils.py
python3 -m pydoc modules/query.py
```

## Authors

Eamon O'Connor (oconnor.eamon0@gmail.com)

## Acknowledgments

Thank you to the GMrepo, Ensembl, and MeSH databases, this script would not be possible without their API's!