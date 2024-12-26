"""
docstring placeholder
"""
import numpy as np
import statistics
import matplotlib.pyplot as plt
import scipy.stats as stats


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


def transform(data, transformation):
    """
    Transform heavily right skewed data to normal distribution.
    @param data: sequence of data to transform
    @param transformation: Type of transformation. Expects 'log10', 'ln', 'boxcox'
    @return data_transformed: sequence of data with given transformation applied
    """
    # Apply appropriate transformation based on input
    if transformation == 'log10':
        data_transformed = np.log10(data)
    elif transformation == 'ln':
        data_transformed = np.log(data)
    elif transformation == 'boxcox':
        data_transformed, data_lambda = stats.boxcox(data)
    else:
        print(f'Invalid transformation type \'{transformation}\'')
        return None

    return data_transformed


def basic_stats(data):
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
    Generates stacked histogram of disease and healthy data
    @param disease_data: Data of disease group to be plotted
    @param health_data: Data of health group to be plotted
    @param pheno_label: Phenotype of disease group
    @param tax_label: Genus of abundance data
    @out_dir: Directory to save histogram to
    @return None
    """
    # Initialize panels
    fig, (ax1, ax2) = plt.subplots(2, sharex=True)

    # Plot disease data
    ax1.hist(disease_data,
             label=pheno_label,
             bins=20,
             color='red')
    
    # Plot health data
    ax2.hist(health_data,
             label='health',
             bins=20,
             color='yellow')
    
    # Add legend
    ax1.legend()
    ax2.legend()

    # Save figure
    plt.savefig(out_dir+'/fig.png', dpi=300)