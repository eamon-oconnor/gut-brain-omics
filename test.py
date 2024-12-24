from modules import query

mesh_id = query.retrieve_mesh_id('Depression')
tax_id, tax_label = query.retrieve_tax_info('Bacteroides')

#print(mesh_id)
#print(tax_id)

query.retrieve_data(mesh_id, tax_id)