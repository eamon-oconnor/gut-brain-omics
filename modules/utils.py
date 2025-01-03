"""
Module including tools to perform analyses of given data. Analyses include
normality transformations, basic statistics, histogram plotting.
"""
import numpy as np
import statistics
import matplotlib.pyplot as plt
import scipy.stats as stats


def transform(data, transformation):
    """
    Transform heavily right skewed data to normal distribution.
    @param data: sequence of data to transform
    @param transformation: Type of transformation. Expects 'log10', 'ln', 'boxcox', 'None'
    @return data_transformed: sequence of data with given transformation applied
    """
    # Apply appropriate transformation based on input
    if transformation == 'log10':
        data_transformed = np.log10(data)
    elif transformation == 'ln':
        data_transformed = np.log(data)
    elif transformation == 'boxcox':
        data_transformed, data_lambda = stats.boxcox(data)
    elif transformation == None:
        data_transformed=data
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
    

def hist(disease_data, health_data, pheno_label, tax_label, transformation, out_dir):
    """
    Generates stacked histogram of disease and healthy data
    @param disease_data: Data of disease group to be plotted
    @param health_data: Data of health group to be plotted
    @param pheno_label: Phenotype of disease group
    @param tax_label: Genus of abundance data
    @param transformation: Type of data transformation
    @param out_dir: Directory to save histogram to
    @return None
    """
    # Initialize panels
    fig, (ax1, ax2) = plt.subplots(2, sharex=True)
    fig.suptitle('Relative Abundance of '+tax_label+' in the Gut Microbiome')

    # Plot disease data
    ax1.hist(disease_data,
             label=pheno_label,
             bins=20,
             color='tab:red')
    ax1.set_ylabel('Frequency')

    # Plot health data
    ax2.hist(health_data,
             label='Health',
             bins=20,
             color='tab:cyan')
    if transformation == None:
        ax2.set_xlabel('Relative Abundance')
    else:
        ax2.set_xlabel('Relative Abundance ('+transformation+' transformation)')
    ax2.set_ylabel('Frequency')
    
    # Add legend
    ax1.legend()
    ax2.legend()

    # Generate plot filename
    fh_hist = tax_label.replace(" ", "-").lower()+'_'+pheno_label.replace(" ", "-").lower()

    # Save figure
    plt.savefig(out_dir+'/'+fh_hist+'_hist.png', dpi=300)