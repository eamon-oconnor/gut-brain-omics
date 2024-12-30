from modules import query
import main

mesh_label = 'Parkinson Disease'
#mesh_id = query.retrieve_mesh_id(mesh_label)
mesh_id = 'D013313'
#mesh_label = query.retrieve_mesh_descriptor(mesh_id)

tax_id, tax_label = query.retrieve_tax_info('Bacteroides')

main.test_pheno_genus(mesh_id, mesh_label,
                      tax_id, tax_label,
                      'boxcox',
                      'two-sided',
                      '/home/eoconnor/Python/Personal_Projects/gut-brain/results')