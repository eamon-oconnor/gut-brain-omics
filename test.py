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
            print(f"No MeSH ID found for descriptor: {mesh_descriptor}")
            return None
    else:
        print(f"Error: {response.status_code}")
        return None


# Example usage
descriptor = "Depresion"
mesh_id = 'D00363'
mesh_id = retrieve_mesh_id(descriptor)
print(f"MeSH ID for '{descriptor}': {mesh_id}")