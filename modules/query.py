"""
docstring
"""
import json
import requests
import pandas as pd
import sys


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
        if len(data)>0 and 'resource' in data[0]:
            mesh_url = data[0]['resource']
            mesh_id = mesh_url[-7:]
            return mesh_id
        else:
            # Raise if unable to find MeSH ID
            raise Exception(f"No MeSH ID found for descriptor: {mesh_descriptor}")
    else:
        # Print and exit if unable to connect to API
        print(f"Unable to connect to database. Status code {response.status_code}")
        sys.exit()


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
        if len(data) > 0:
            mesh_descriptor = data[0]
            return mesh_descriptor
        else:
            # Raise if unable to find MeSH ID
            raise Exception(f"MeSH ID \'{mesh_id}\' not found")
    else:
        # Print and exit if unable to connect to API
        print(f"Unable to connect to database. Status code {response.status_code}")
        sys.exit()


def retrieve_tax_info(tax_in):
    """
    Retrieves NIH taxonomy ID and name of species/genus
    @param tax_in: Scientific name or NIH tax ID of species/genus
    @return tax_id: NIH taxonomy ID of species/genus
    @return tax_name: Scientific name of species/genus
    """
 
    server = "https://rest.ensembl.org"
    ext = "/taxonomy/id/"+str(tax_in)+"?"
    
    response = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
    
    # Check if the response status is OK
    if response.status_code == 200:
        decoded = response.json()
        tax_name = decoded['name']
        tax_id = decoded['id']

        return(tax_id, tax_name)
    else:
        print(f'NIH Taxonomy ID or name \'{tax_in}\' not found.')
        raise Exception


def retrieve_data(mesh_id, tax_id, mesh_label, tax_label):
    """
    Retrieves gut microbiome abundance data of given species/genus associated with given phenotype (courtesy of GMrepo)
    @param mesh_id: MeSH ID of phenotype (see NIH)
    @param tax_id: NCBI taxonomy ID of species/genus
    @param mesh_label: Descriptive name of phenotype (Depression, Anxiety, etc.)
    @param tax_label: Scientific name of species/genus
    @return disease_data: relative abundances of the species/genus of interests in all samples of phenotype (vector)
    @return health_data: relative abundances of the species/genus of interests in all samples of Health (vector)
    """

    # Retrieve dataset from GMrepo
    data_query = {'mesh_id': mesh_id,"ncbi_taxon_id" : tax_id}
    url = 'https://gmrepo.humangut.info/api/getMicrobeAbundancesByPhenotypeMeshIDAndNCBITaxonID'
    data = requests.post(url, data=json.dumps(data_query))

    # Check if the response status is OK
    if data.status_code == 200:

        # Select disease abundance data
        disease_data = pd.DataFrame(data.json().get('abundant_data_for_disease'))

        # Select health abundance data
        health_data = pd.DataFrame(data.json().get('abundant_data_for_health'))

        # Check that data was successfully retrieved
        if len(disease_data) > 0 and len(health_data) > 0:
            return(disease_data.values.flatten(), health_data.values.flatten())
        else:
            # Raise if unable to pull data
            print(f"{mesh_label} and/or {tax_label} not found in GMRepo database.")
            raise Exception
    else:
        # Print and exit if unable to connect to API
        print(f"Unable to connect to database. Status code {data.status_code}")
        sys.exit()