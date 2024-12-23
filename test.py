import requests,sys

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

        return(tax_name, tax_id)

    else:
        print(f'NIH Taxonomy ID or name \'{tax_in}\' not found.')
        return None

print(retrieve_tax_info('homo sapiens'))