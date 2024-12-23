"""
docstring
"""
import json
import requests


def retrieve_mesh_id(mesh_descriptor):
    """
    Retrives MeSH phenotype id from descriptive name
    @param mesh_descriptor: Descriptive name of phenotype (Depression, Anxiety, etc.)
    @return mesh_id: MeSH ID of phenotype
    """

    # Base URL for MeSH Lookup API
    base_url = "https://id.nlm.nih.gov/mesh/lookup/descriptor"

    # Send a GET request to the API with the descriptor name
    response = requests.get(base_url, params={'label': mesh_descriptor})

    # Check if the response status is OK
    if response.status_code == 200:
        # Parse the response JSON
        data = response.json()

        # Check if the descriptor was found and retrieve the MeSH ID
        if 'resource' in data[0]:
            mesh_url = data[0]['resource']
            mesh_id = mesh_url[-7:]
            return mesh_id
        else:
            return f"No MeSH ID found for descriptor: {mesh_descriptor}"
    else:
        return f"Error: {response.status_code}"


def retrieve_mesh_descriptor(mesh_id):
    """
    Retrives MeSH phenotype descriptor from id
    @param mesh_id: NIH MeSH ID of phenotype
    @return mesh_descriptor: Descriptive name of phenotype (Depression, Anxiety, etc.)
    """
    # Base URL for MeSH Lookup API
    base_url = "https://id.nlm.nih.gov/mesh/lookup/label"

    # Send a GET request to the API with the id
    response = requests.get(base_url, params={'resource': mesh_id})

    # Check if the response status is OK
    if response.status_code == 200:
        # Parse the response JSON
        data = response.json()

        # Retrieve the MeSH ID
        mesh_descriptor = data[0]
        return mesh_descriptor
    else:
        return f"Error: {response.status_code}"


def retrieve_tax_id()


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