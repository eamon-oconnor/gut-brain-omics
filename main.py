"""
docstring placeholder
"""

from modules import utils, query
import argparse
import pandas as pd
import scipy.stats as stats


def test_pheno_genus(mesh_id, mesh_label, tax_id, tax_label, out_dir):
    """
    Pull data from GMrepo for given mesh/tax, print stats, make hist
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

    # Normal Transformation
    disease_data = utils.transform(disease_data)
    health_data = utils.transform(health_data)

    # Check Normality


    # Calculate means and standard deviations
    disease_mean, disease_stdev = utils.stats(disease_data)
    health_mean, health_stdev = utils.stats(health_data)

    # Perform Welch t-test
    p_value = stats.ttest_ind(disease_data, health_data, equal_var = False, alternative='less').pvalue

    # Generate histogram
    utils.hist(disease_data, health_data, mesh_label, tax_label, out_dir)

    # Print stats
    print(f'The sample size in the {mesh_label} group is {disease_n}, while that of the health group is {health_n}.')
    print(f'The mean relative abundance of {tax_label} in the {mesh_label} group is {round(disease_mean,3)}, with a standard deviation of {round(disease_stdev,3)}.')
    print(f'The mean relative abundance of {tax_label} in the health group is {round(health_mean,3)}, with a standard deviation of {round(health_stdev,3)}.')
    print(f'A Welch\'s t-test of {tax_label} abundance between the {mesh_label} group and healthy group produced a p-value of {p_value:.3e}.')


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