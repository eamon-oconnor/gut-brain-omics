"""
docstring placeholder
"""
import pandas as pd
import statistics
from . import query
import scipy.stats as sci_stats 


def df_to_list(df):
    """
    Converts dataframe to dictionary of lists with each column name being a key
    @param csv_path: absolute or relative filepath to csv file
    @return: csv_dict
    """
    csv_dict = {}

    for column, data in df.iteritems():
        csv_dict[column] = data
    
    return csv_dict


def stats(data):
    """
    Calculates mean and standard deviation for a given dataset
    @param data: sequence of data values
    @return mean: calculated mean of data
    @st_dev: calculated standard deviation of data
    """
    mean = statistics.mean(data)
    st_dev = statistics.stdev(data)

    return mean, st_dev
    

def hist():
    """
    
    """


def test_pheno_genus(mesh_id, mesh_label, tax_id, tax_label):
    """
    Main function. Pull data from GMrepo for given mesh/tax, print stats, make hist
    @param mesh_id: NIH MeSH ID of phenotype
    @param mesh_label: Descriptive name of phenotype (Depression, Anxiety, etc.)
    @param tax_id: NIH taxonomy ID of species/genus
    @param tax_name: Scientific name of species/genus
    @param hist_dir: directory to write histogram to
    @return None
    """
    # Retrieve data
    disease_data, health_data = query.retrieve_data(mesh_id, tax_id)

    print(disease_data)
    # Calculate means and standard deviations
    disease_mean, disease_stdev = stats(disease_data)
    health_mean, health_stdev = stats(health_data)

    # Perform Welch t-test
    p_value = sci_stats.ttest_ind(disease_data, health_data, equal_var = False)

    # Print stats
    print(f'The mean relative abundance of {tax_label} in the {mesh_label} group is {disease_mean},\
          with a standard deviation of {disease_stdev}.')
    print(f'A Welch\'s t-test of {tax_label} abundance between the {mesh_label} group and \
          healthy group produced a p-value of {p_value}.')