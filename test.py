import requests

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

# Example usage
descriptor = "Depression"
mesh_id = 'D003863'
mesh_descriptor = retrieve_mesh_descriptor(mesh_id)
print(f"MeSH ID for '{mesh_descriptor}': {mesh_id}")