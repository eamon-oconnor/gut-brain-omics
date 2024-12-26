"""
docstring placeholder
"""

from modules import utils, query
import argparse
import pandas as pd
import scipy.stats as stats


def test_pheno_genus(mesh_id, mesh_label, tax_id, tax_label, transformation, hist_dir):
    """
    Pull data from GMrepo for given mesh/tax, print stats, make hist
    @param mesh_id: NIH MeSH ID of phenotype
    @param mesh_label: Descriptive name of phenotype (Depression, Anxiety, etc.)
    @param tax_id: NIH taxonomy ID of species/genus
    @param tax_label: Scientific name of species/genus
    @param transformation: Type of transformation to apply to data. Expects 'log10', 'ln', 'boxcox'
    @param hist_dir: directory to write histogram to
    @return None
    """
    # Retrieve data
    disease_data, health_data = query.retrieve_data(mesh_id, tax_id)

    # Normal Transformation
    disease_norm = utils.transform(disease_data, transformation)
    health_norm = utils.transform(health_data, transformation)

    # Check Normality
    #p_norm_disease = stats.shapiro(disease_norm).pvalue
    #p_norm_health = stats.shapiro(health_norm).pvalue

    # Calculate means and standard deviations
    disease_mean, disease_stdev = utils.basic_stats(disease_data)
    health_mean, health_stdev = utils.basic_stats(health_data)

    # Perform Welch t-test if transformed data is normal
    #if p_norm_disease > 0.05 and p_norm_health > 0.05:
    p_welch = stats.ttest_ind(disease_norm, health_norm, equal_var = False, alternative='less').pvalue
    #    norm = True
    #else:
    #    norm = False

    norm=True

    # Generate histogram
    utils.hist(disease_norm, health_norm, mesh_label, tax_label, hist_dir)

    # Print stats
    print(f'The mean relative abundance of {tax_label} in the {mesh_label} group is {round(disease_mean,3)}, with a standard deviation of {round(disease_stdev,3)}.')
    print(f'The mean relative abundance of {tax_label} in the health group is {round(health_mean,3)}, with a standard deviation of {round(health_stdev,3)}.')
    if norm == True:
        print(f'A Welch\'s t-test of {tax_label} abundance between the {mesh_label} group and healthy group produced a p-value of {p_welch:.3e}.')
    elif norm == False:
        print(f'A Shapiro-Wilk test for normality yielded a p-value of {p_norm_disease} for the {mesh_label} group and {p_norm_health} for the health group. At least one dataset is not normal and a Welch\'s t-test cannot be performed.')


def get_fh_argparse():
    """
    Get file handle command line options using argparse
    @param: NoneType
    @return: ArgumentParser
    """

    parser = argparse.ArgumentParser(
        description="Provide phenotype and genus or CSV file"
    )

    parser.add_argument(
        "-i",
        "--infile",
        dest="infile",
        type=str,
        help="Path to file to open",
        required=False,
    )

    parser.add_argument(
        "-p",
        "--phenotype",
        dest="phenotype",
        type=str,
        help="Phenotype to analyze",
        required=False,
    )

    parser.add_argument(
        "-g",
        "--genus",
        dest="genus",
        type=str,
        help="Genus or species to analyze",
        required=False,
    )

    parser.add_argument(
        "-o",
        "--outdir",
        dest="outdir",
        type=str,
        help="Path to directory to write results to",
        required=True,
    )

    # Execute parse_args() method
    return parser.parse_args()


def main():
    """ main """

    # Get infile and out directory from cdl
    args = get_fh_argparse()
    if args.infile():
        csv_fh = args.infile
    result_dir = args.outdir

    # Convert csv to df
    df = pd.read_csv(csv_fh)

    # Loop through df rows
    #for index, row in df.iterrows():