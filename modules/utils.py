"""
docstring placeholder
"""
import numpy as np
import statistics
from . import query
import scipy.stats as sci_stats 
import matplotlib.pyplot as plt
import random


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


def transform(data):
    """
    
    """
    log_data = np.log(data)
    return log_data


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
    

def hist(disease_data, health_data, pheno_label, tax_label, out_dir):
    """
    
    """
    #health_adj = random.sample(sorted(health_data), len(disease_data))

    fig, (ax1, ax2) = plt.subplots(2, sharex=True)

    ax1.hist(disease_data,
             label=pheno_label,
             bins=20,
             color='red')
    
    ax2.hist(health_data,
             label='health',
             bins=20,
             color='yellow')
    
    plt.legend()

    #plt.show()
    plt.savefig(out_dir+'/fig.png',
                dpi=300)


def test_pheno_genus(mesh_id, mesh_label, tax_id, tax_label, out_dir):
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

    # Find sample sizes
    disease_n = len(disease_data)
    health_n = len(health_data)

    # Transformation
    disease_data = transform(disease_data)
    health_data = transform(health_data)
    #disease_data, disease_lambda = sci_stats.boxcox(disease_data)
    #health_data, health_lambda = sci_stats.boxcox(health_data)


    # Calculate means and standard deviations
    disease_mean, disease_stdev = stats(disease_data)
    health_mean, health_stdev = stats(health_data)

    # Perform Welch t-test
    p_value = sci_stats.ttest_ind(disease_data, health_data, equal_var = False, alternative='less').pvalue

    # Generate histogram
    hist(disease_data, health_data, mesh_label, tax_label, out_dir)

    # Print stats
    print(f'The sample size in the {mesh_label} group is {disease_n}, while that of the health group is {health_n}.')
    print(f'The mean relative abundance of {tax_label} in the {mesh_label} group is {round(disease_mean,3)}, with a standard deviation of {round(disease_stdev,3)}.')
    print(f'The mean relative abundance of {tax_label} in the health group is {round(health_mean,3)}, with a standard deviation of {round(health_stdev,3)}.')
    print(f'A Welch\'s t-test of {tax_label} abundance between the {mesh_label} group and healthy group produced a p-value of {p_value:.3e}.')