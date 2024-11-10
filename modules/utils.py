"""
docstring placeholder
"""
import pandas as pd
import json
import requests

def csv_to_list(csv_path):
    """
    Reads csv files, returns dictionary of lists with each column name being a key
    @param csv_path: absolute or relative filepath to csv file
    @return: csv_dict
    """
    df = pd.read_csv(csv_path)


def retrieve_data(mesh_id, tax_id):
    """
    Retrieves gut microbiome abundance data of given species/genus associated with given phenotype (courtesy of GMrepo)
    @param mesh_id: MeSH ID of phenotype (see NIH)
    @param tax_id: NCBI taxonomy ID of species/genus
    @return data: list containing following dataframes:
        hist_data_for_phenotype: relative abundances of the species/genus of interests in all samples of phenotype (dataframe)
        hist_data_for_health: relative abundances of the species/genus of interests in all samples of Health (dataframe)
        abundant_data_for_disease: relative abundances of the species/genus of interests in all samples of phenotype (vector)
        abundant_data_for_health: relative abundances of the species/genus of interests in all samples of Health (vector)
        taxon: NCBI taxonomy information
        disease: details of current phenotype
        abundance_and_meta_data: runs in which current taxon is found and related meta data
        co_occurred_taxa: cooccurred taxa of the taxon of interests in current phenotype
    """
    data_query = {'mesh_id': mesh_id,"ncbi_taxon_id" : tax_id}
    url = 'https://gmrepo.humangut.info/api/getMicrobeAbundancesByPhenotypeMeshIDAndNCBITaxonID'
    data = requests.post(url, data=json.dumps(data_query))

    return data


def stats():


def t_test():


def write_csv():
    

def hist():