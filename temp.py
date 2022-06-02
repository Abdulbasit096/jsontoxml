# import xml.etree.cElementTree as ET
# import json

# with open('URLA-Smith.json') as urla_json:
#     urla_data = dict(json.load(urla_json))

# # creates xml roots and it's properties
# XML_ROOT = ET.Element('MESSAGE')
# root.set('MISMOReferenceModelIdentifier', '3.4.032420160128')
# root.set('xmlns','http://www.mismo.org/residential/2009/schemas')
# root.set('xmlns:ULAD','http://www.datamodelextension.org/Schema/ULAD')
# root.set('xmlns:xlink',"http://www.w3.org/1999/xlink")
# root.set('xmlns:xsi','http://www.w3.org/2001/XMLSchema-instance')

# ABOUT_VERSIONS = ET.SubElement(root, 'ABOUT_VERSIONS')
# ABOUT_VERSION = ET.SubElement(ABOUT_VERSION, 'ABOUT_VERSION')
# created_date = ET.SubElement(ABOUT_VERSION, 'CreatedDatetime')

# DEAL_SETS = ET.SubElement(root, 'DEAL_SETS')
# DEAL_SET = ET.SubElement(DEAL_SETS, 'DEAL_SET')


# def section_one():
#     borrower_information = urla_data['section_1']
#     section_one_A(borrower_information)


# def section_one_A(borrower_information):
    

obj = {
    'name': 'John Smith',
    'age' : 18,
}
# copy elements of obj into second dictonary
new_obj = obj.copy()
print(new_obj)