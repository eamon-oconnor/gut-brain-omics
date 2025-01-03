# Project Title

gut-brain-omics

## Description





The program get_gene_level_information will take a host and gene name. The program prints a formatted list of tissues where the given gene is expressed in the given host, looked up from a local unigene data file.

The program includes a function titled update_host_name, which takes an input host name and returns the host name formatted for file lookup. The function will print a list of acceptable host names and exit if the host name is not found. The program also includes a function titled _print_directories_for_hosts, which prints a list of acceptable host names and exits the program. The function get_data_for_gene_file takes a unigene filepath and returns an alphabetical list of tissues the gene is expressed in. The function print_host_to_gene_name_output takes a host name passed from the command line, a gene name passed from the command line, and a list of tissues that gene is expressed in, and prints a formatted list of tissues. The program's last function is titled get_fh_argparse, which will return an ArgumentParser object containing a host name and gene name entered in the command line.

The program imports functions from the io_utils.py module. The module includes a function titled get_filehandle, which takes a file name and open mode and returns a file handle to be used. The module also includes a function titled is_gene_file_valid, which takes a file name and returns True if the file path exists and False otherwise.

The program also imports functions from the config.py module. The module includes functions titled get_directory_for_unigene and get_extension_for_unigene, which return the unigene data directory and file extension. These strings are set as global variables in the module. The module also includes a function titled get_keywords_for_hosts, which returns a dictionary with common and scientific host names as keys and scientific names formatted for file directory as values. The module also has functions titled get_error_string_4_opening_file_os_error, get_error_string_4_value_error, and get_error_string_4_type_error. These functions print the error string for their respective errors.

There are also test functions for the io_utils.py module and config.py moedule attached. The test programs include unit test functions for each function in the module which can be run with pytest to verify that each function is working as intended. There is also a .coveragerc file attached to configure pytest.

## Getting Started

### Dependencies

The project was written on the Ubuntu Linux opersating system on Python 3.10.12. It uses the argparse, pandas, scipy, statsmodels, pylab, sys, numpy, statistics, matplotlib, json, requests, and sys libraries.

### Installing

The program files can be cloned from github: "https://github.com/eamon-oconnor/gut-brain-omics"

### Executing program

The program get_gene_level_information.py can be run from the command line with the following format:
```
python3 get_gene_level_information.py --host "host name" --gene "gene name"
```
Accepted hosts for analysis include homo sapiens, bos taurus, equus caballus, mus musculus, ovis aries, and rattus norvegicus.

The program can also be run without specifying a host and gene, in which case the default values "Human" and "TGM1" will be used. An example of a command line input and output for the program would be:
```
python3 get_gene_level_information.py --host horse --gene API5

Found Gene API5 for Equus caballus
In Equus caballus, there are 3 tissues that API5 is expressed in:

  1. Adult
  2. Blood
  3. Cartilage
```

## Help

An error will be returned if the module io_utils.py or config.py is not found within the relative directory assignment5/ with __init__.py present in the same directory. An error would also be returned if the unigene data directory/extension specified in the config.py file are not found. Any errors would likely be resolved by confirming that the required modules are present, and that any data files are in the specified directory.

If a host name is input that is not found in the database, a list of acceptable host names will be output by the program. If a gene name is input that does not exist for the given host, the program will exit.

The following command line input can be run for more information on the arguments and usage of the program find_common_cats.py:
```
python3 get_gene_level_information.py -h
```

The following command line inputs can be run for information on the arguments, parameters, and return of the programs functions:
```
help(update_host_name)
help(_print_directories_for_hosts)
help(get_data_for_gene_file)
help(print_host_to_gene_name_output)
help(get_fh_argparse)
help(get_filehandle)
help(is_gene_file_valid)
help(get_directory_for_unigene)
help(get_extension_for_unigene)
help(get_keywords_for_hosts)
help(get_error_string_4_opening_file_os_error)
help(get_error_string_4_value_error)
help(get_error_string_4_type_error)
```

The following command line inputs can be run for more information on the project modules:
```
python3 -m pydoc modules/utils.py
python3 -m pydoc modules/query.py
```

## Authors

Eamon O'Connor (oconnor.eamon0@gmail.com)

## Acknowledgments

