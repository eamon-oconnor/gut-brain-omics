"""
docstring placeholder
"""

from modules import utils, query
import argparse
import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm 
import pylab as py
import sys


def test_pheno_genus(mesh_id,
                     mesh_label,
                     tax_id, tax_label,
                     transformation,
                     alternative,
                     out_dir):
    """
    Pull data from GMrepo for given mesh/tax, print stats, make hist
    @param mesh_id: NIH MeSH ID of phenotype
    @param mesh_label: Descriptive name of phenotype (Depression, Anxiety, etc.)
    @param tax_id: NIH taxonomy ID of species/genus
    @param tax_label: Scientific name of species/genus
    @param transformation: Type of transformation to apply to data. Expects 'log10', 'ln', 'boxcox'
    @param alternative: Alternative hypothesis of comparison. Expects 'two-sided', 'greater', 'less'
    @param out_dir: directory to write plots to
    @return None
    """
    # Retrieve data
    disease_data, health_data = query.retrieve_data(mesh_id, tax_id, mesh_label, tax_label)

    # Break if data unable to be retrieved
    if disease_data is None or health_data is None:
        return None

    # Normal Transformation
    disease_norm = utils.transform(disease_data, transformation)
    health_norm = utils.transform(health_data, transformation)

    # Generate plot filenames
    fh_disease = tax_label.replace(" ", "-").lower()+'_'+mesh_label.replace(" ", "-").lower()
    fh_health = tax_label.replace(" ", "-").lower()+'_health'

    # QQ Plots to check Normality
    sm.qqplot(health_norm, line ='45')
    py.title('Q-Q Plot: ' + tax_label + ", Health")
    py.savefig(out_dir+'/'+fh_health+'_qq.png', dpi=300)
    
    py.clf()
    
    sm.qqplot(disease_norm, line ='45')
    py.title('Q-Q Plot: ' + tax_label + ", " + mesh_label)
    py.savefig(out_dir+'/'+fh_disease+'_qq.png', dpi=300)

    # Calculate means and standard deviations
    disease_mean, disease_stdev = utils.basic_stats(disease_data)
    health_mean, health_stdev = utils.basic_stats(health_data)

    # Perform Welch t-test
    p_welch = stats.ttest_ind(disease_norm, health_norm, equal_var = False, alternative=alternative).pvalue
    
    # Mann Whitney U Test
    p_mw = stats.mannwhitneyu(disease_data, health_data, alternative=alternative).pvalue

    # Generate histogram
    utils.hist(disease_norm, health_norm, mesh_label, tax_label, transformation, out_dir)

    # Print stats
    print(f'The mean relative abundance of {tax_label} in the {mesh_label} group is {round(disease_mean,3)}, with a standard deviation of {round(disease_stdev,3)}.')
    print(f'The mean relative abundance of {tax_label} in the health group is {round(health_mean,3)}, with a standard deviation of {round(health_stdev,3)}.')
    print(f'A Welch\'s t-test of {tax_label} abundance between the {mesh_label} group and healthy group produced a p-value of {p_welch:.3e}.')
    print(f'A Mann-Whitney U test of {tax_label} abundance between the {mesh_label} group and healthy group produced a p-value of {p_mw:.3e}.')


def pull_mesh(mesh):
    """
    Pulls MeSH ID & label from API given either ID or label. Nested if/else and try/except structure to reduce superfluous API requests
    @param mesh: MeSH ID or label
    @return mesh_id: MeSH ID
    @return mesh_label: MeSH label
    """
    # Test for MeSH ID characteristics
    if len(mesh) == 7 and mesh[0] == 'D':
        # Likely MeSH ID input
        try:
            mesh_label = query.retrieve_mesh_descriptor(mesh)
            mesh_id = mesh
        except:
            # Try MeSH label
            try:
                mesh_id = query.retrieve_mesh_id(mesh)
                mesh_label = mesh
            except:
                print(f'MeSH label or ID {mesh} not found.')
                raise Exception
    else:
        # Likely MeSH label input
        try:
            mesh_id = query.retrieve_mesh_id(mesh)
            mesh_label = mesh
        except:
            # Try MeSH ID
            try:
                mesh_label = query.retrieve_mesh_descriptor(mesh)
                mesh_id = mesh
            except:
                print(f'MeSH label or ID {mesh} not found.')
                raise Exception
    
    return mesh_id, mesh_label


def process_csv(csv, transformation, alternative, out_dir):
    """
    Loop through given CSV, analyze contained phenotypes and genera
    @param csv: Directory of input CSV
    @param transformation: Type of transformation to apply to data. Expects 'log10', 'ln', 'boxcox'
    @param alternative: Alternative hypothesis of comparison. Expects 'two-sided', 'greater', 'less'
    @param out_dir: directory to write plots to
    @return None
    """
    # Read to dataframe (try/except)
    try:
        df = pd.read_csv(csv)
    except:
        print(f'Input CSV directory does not exist or is not a CSV.')
        return

    # Check that Phenotype and Genus columns exist
    if set('Phenotype','Genus').issubset(df.columns):
        # Loop through df
        for index, row in df.iterrows():
            try:
                # Set phenotype and genus
                pheno = row['Phenotype']
                genus = row['Genus']

                # Pull mesh id and label
                mesh_id, mesh_label = pull_mesh(pheno)
                        
                # Pull taxonomy id and label
                tax_id, tax_label = query.retrieve_tax_info(genus)

                # Run analysis
                test_pheno_genus(
                    mesh_id,
                    mesh_label,
                    tax_id,
                    tax_label,
                    transformation,
                    alternative,
                    out_dir
                )
            except:
                pass
    else:
        print(f'Input CSV must include columns labeled \'Phenotype\' and \'Genus\'')


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
        help="Path to CSV file to open",
        required=False,
        default=None
    )

    parser.add_argument(
        "-p",
        "--phenotype",
        dest="phenotype",
        type=str,
        help="Phenotype to analyze",
        required=False,
        default=None
    )

    parser.add_argument(
        "-g",
        "--genus",
        dest="genus",
        type=str,
        help="Genus or species to analyze",
        required=False,
        default=None
    )

    parser.add_argument(
        "-o",
        "--outdir",
        dest="outdir",
        type=str,
        help="Path to directory to write results to",
        required=True,
    )

    parser.add_argument(
        "-t",
        "--transformation",
        dest="transformation",
        type=str,
        help="Transformation type for normalization. Options are 'boxcox', 'log10', 'ln', and 'None'",
        required=False,
        default='boxcox'
    )

    parser.add_argument(
        "-a",
        "--alternative",
        dest="alternative",
        type=str,
        help="Alternative hypothesis for comparison between phenotype and health groups. Options are 'two-sided', 'greater', 'less'",
        required=False,
        default='two-sided'
    )

    # Execute parse_args() method
    return parser.parse_args()


def main():
    """main"""

    # Get args from cdl
    args = get_fh_argparse()
    
    # Set arguments to variables
    csv = args.infile
    pheno = args.phenotype
    genus = args.genus
    outdir = args.outdir
    transf = args.transformation
    alt = args.alternative
    
    # Check if a CSV was given
    if csv is None:
        is_csv = False
    else:
        is_csv = True
    
    # Check if a pheno/genus pair was given
    if pheno is None or genus is None:
        is_pg = False
    else:
        is_pg = True

    # Exit if no CSV and no pheno/genus pair
    if is_csv == False and is_pg == False:
        print(f'Please input either a CSV filepath or a phenotype/genus pair.')
        sys.exit()

    # Process input Pheno/Genus pair
    if is_pg == True:
        try:
            # Pull mesh id and label
            mesh_id, mesh_label = pull_mesh(pheno)
                    
            # Pull taxonomy id and label
            tax_id, tax_label = query.retrieve_tax_info(genus)

            # Run analysis
            test_pheno_genus(
                mesh_id,
                mesh_label,
                tax_id,
                tax_label,
                transf,
                alt,
                outdir
            )
        except:
            pass

    # Process CSV
    if is_csv == True:
        process_csv(csv, transf, alt, outdir)


if __name__ == "__main__":
    main()
