"""
docstring placeholder
"""
import pandas as pd
import statistics
from . import query
import scipy.stats as sci_stats 
import matplotlib.pyplot as plt


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
    

def hist(disease_data, health_data, pheno_label, tax_label):
    """
    
    """
    plt.hist(disease_data,bins=100)
    plt.hist(health_data,bins=100)

    plt.show()


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

    # Calculate means and standard deviations
    disease_mean, disease_stdev = stats(disease_data)
    health_mean, health_stdev = stats(health_data)

    # Perform Welch t-test
    p_value = sci_stats.ttest_ind(disease_data, health_data, equal_var = False, alternative='less').pvalue

    # Generate histogram
    hist(disease_data, health_data, mesh_label, tax_label)

    # Print stats
    print(f'The mean relative abundance of {tax_label} in the {mesh_label} group is {round(disease_mean,3)}, with a standard deviation of {round(disease_stdev,3)}.')
    print(f'The mean relative abundance of {tax_label} in the health group is {round(health_mean,3)}, with a standard deviation of {round(health_stdev,3)}.')
    print(f'A Welch\'s t-test of {tax_label} abundance between the {mesh_label} group and healthy group produced a p-value of {p_value:.3e}.')