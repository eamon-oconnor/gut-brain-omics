import requests

def get_mesh_term_by_id(mesh_id):
    url = f"https://id.nlm.nih.gov/mesh/lookup/descriptor/{mesh_id}.json"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        term = data.get('label', 'No label found')
        return term
    else:
        return f"Error: {response.status_code}"

# Example usage
mesh_id = 'D003863'  # This is an example MeSH ID
term = get_mesh_term_by_id(mesh_id)
print(f"MeSH Term for {mesh_id}: {term}")
