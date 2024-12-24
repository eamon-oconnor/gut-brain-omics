from modules import query
from modules import utils

mesh_label = 'Depression'
mesh_id = query.retrieve_mesh_id(mesh_label)
#mesh_id = 'D013313'
#mesh_label = query.retrieve_mesh_descriptor(mesh_id)

tax_id, tax_label = query.retrieve_tax_info('Bacteroides')

utils.test_pheno_genus(mesh_id, mesh_label, tax_id, tax_label)