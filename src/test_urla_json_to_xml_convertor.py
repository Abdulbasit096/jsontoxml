import unittest
import xml.etree.ElementTree as ET
import urla_json_to_xml_convertor as jtox
from config import get_project_root
import json


class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.case_id = jtox.case_id
        cls.leadingStr = '{http://www.mismo.org/residential/2009/schemas}'
        cls.convertedXml = open(f'{get_project_root()}/test_resources/{cls.case_id}.xml', 'r')
        cls.convertedRoot = ET.parse(cls.convertedXml).getroot()
        cls.actualXml = open(f'{get_project_root()}/test_resources/{cls.case_id}_actual.xml', 'r')
        cls.actualRoot = ET.parse(cls.actualXml).getroot()

    @classmethod
    def tearDownClass(cls):
        cls.actualXml.close()
        cls.convertedXml.close()

    def setUp(self):
        self.actual_deal_path = self.actualRoot[1][0][0][0]
        self.converted_deal_path = self.convertedRoot[1][0][0][0]
        self.actual_party_path = self.actual_deal_path[4][0]
        self.converted_party_path = self.converted_deal_path[4][0]
        self.actual_roles_path = self.actual_party_path[3]
        self.converted_roles_path = self.converted_party_path[2]

    def test_YesNoToBoolean(self):
        actual_one = jtox.YesNOtoBoolean('Yes')
        expected_one = 'true'
        actual_two = jtox.YesNOtoBoolean('no')
        expected_two = 'false'
        actual_three = jtox.YesNOtoBoolean(None)
        self.assertEqual(expected_one, actual_one)
        self.assertEqual(expected_two, actual_two)
        self.assertIsNone(actual_three)

    def test_checkIfJsonExist(self):
        file = open(f'{get_project_root()}/test_resources/test.json', 'r')
        data = dict(json.load(file))
        actual = jtox.checkIfJsonExist(data, 'name')
        expected = data['name']
        self.assertEqual(expected, actual)
        actual_two = jtox.checkIfJsonExist(data, 'age')
        self.assertIsNone(actual_two)
        file.close()

    def test_compare_roots(self):
        jtox.createRoot()
        self.assertEqual(self.convertedRoot.tag, self.actualRoot.tag)

    def test_compare_root_attr(self):
        self.assertEqual(self.convertedRoot.attrib, self.actualRoot.attrib)

    def test_compare_root_children(self):
        actual = [x.tag for x in self.actualRoot]
        converted = [y.tag for y in self.convertedRoot]
        self.assertEqual(converted, actual)

    def test_deal_children(self):
        self.assertEqual(self.converted_deal_path.tag, self.actual_deal_path.tag)
        actual_deal_children = [x.tag for x in self.actual_deal_path]
        converted_deal_children = [x.tag for x in self.converted_deal_path]
        self.assertEqual(converted_deal_children, actual_deal_children)

    def test_assets(self):
        # Dont have complete info on Assets
        pass

    def test_collaterals(self):
        actual_collaterals_path = self.actual_deal_path[1][0][0]
        converted_collaterals_path = self.converted_deal_path[1][0][0]
        actual_collateral_children = [x.tag for x in actual_collaterals_path]
        converted_collateral_children = [x.tag for x in converted_collaterals_path]
        self.assertEqual(len(converted_collateral_children), len(actual_collateral_children))
        self.assertEqual(converted_collateral_children, actual_collateral_children)
        actual_address = [x.text for x in actual_collaterals_path.find(f'{actual_collateral_children[0]}')]
        actual_property_details = [x.text for x in actual_collaterals_path.find(f'{actual_collateral_children[1]}')]
        actual_property_valuations = [x.text for x in
                                      actual_collaterals_path.find(f'{actual_collateral_children[2]}')[0][0][0]]
        converted_address = [x.text for x in converted_collaterals_path.find(f'{converted_collateral_children[0]}')]
        converted_property_details = [x.text for x in
                                      converted_collaterals_path.find(f'{converted_collateral_children[1]}')]
        converted_property_valuations = [x.text for x in
                                         converted_collaterals_path.find(f'{converted_collateral_children[2]}')[0][0][
                                             0]]
        self.assertEqual(converted_address, actual_address)
        self.assertEqual(converted_property_details, actual_property_details)
        self.assertEqual(converted_property_valuations, actual_property_valuations)

    def test_liablities(self):
        # Dont have complete info on Liabs
        pass

    def test_loans(self):
        # Dont have complete info on Loans
        pass

    def test_parties_children(self):
        actual_party_children = [x.tag for x in self.actual_party_path]
        converted_party_children = [x.tag for x in self.converted_party_path]
        self.assertEqual(len(converted_party_children), len(actual_party_children))
        self.assertEqual(converted_party_children, actual_party_children)

    def test_parties_individual_contact_points(self):
        actual_individual_path = self.actual_deal_path[4][0][0]
        converted_individual_path = self.converted_deal_path[4][0][0]
        self.assertEqual(len(converted_individual_path), len(actual_individual_path))
        self.assertEqual(converted_individual_path.tag, actual_individual_path.tag)
        actual_contact_points_path = actual_individual_path[0]
        converted_contact_points_path = converted_individual_path[0]
        actual_contact_points = []
        converted_contact_points = []
        for i in range(len(converted_contact_points_path)):
            for j in range(len(converted_contact_points_path[i])):
                converted_contact_points.append(converted_contact_points_path[i][j][0].text)

        for i in range(len(actual_contact_points_path)):
            for j in range(len(actual_contact_points_path[i])):
                actual_contact_points.append(actual_contact_points_path[i][j][0].text)

        self.assertEqual(converted_contact_points, actual_contact_points)

    def test_parties_individual_name(self):
        # Ask Owais Bhai this
        actual_individual_path = self.actual_deal_path[4][0][0]
        converted_individual_path = self.converted_deal_path[4][0][0]
        actual_name_path = actual_individual_path[1]
        converted_name_path = converted_individual_path[1]
        actual_name = ''
        actual_name_tags = []
        converted_name = ''
        converted_name_tags = []
        for i in range(len(converted_name_path)):
            converted_name += f' {converted_name_path[i].text}'
            converted_name_tags.append(converted_name_path[i].tag)
        for i in range(len(actual_name_path)):
            actual_name += f' {actual_name_path[i].text}'
            actual_name_tags.append(actual_name_path[i].tag)
        self.assertEqual(converted_name, actual_name)
        self.assertEqual(converted_name_tags, actual_name_tags)

    def test_parties_address(self):
        actual_address_path = self.actual_party_path[1][0]
        converted_address_path = self.converted_party_path[1][0]
        actual_address = [x.text for x in actual_address_path]
        converted_address = [x.text for x in converted_address_path]
        self.assertEqual(converted_address, actual_address)

    def test_parties_roles_borrower_borrowerDetails(self):
        actual_borrower_details_path = self.actual_roles_path[0][0][0]
        converted_borrower_details_path = self.converted_roles_path[0][0][0]
        actual_borrower_details = [x.text for x in actual_borrower_details_path]
        converted_borrower_details = [x.text for x in converted_borrower_details_path]
        actual_borrower_details.sort()
        converted_borrower_details.sort()
        self.assertEqual(converted_borrower_details, actual_borrower_details)

    def test_parties_roles_borrower_currentIncome(self):
        actual_current_income_items_path = self.actual_roles_path[0][0][1][0]
        converted_current_income_items_path = self.converted_roles_path[0][0][1][0]
        actual_current_income_items = []
        converted_current_income_items = []
        for x in range(len(actual_current_income_items_path)):
            for y in range(len(actual_current_income_items_path[x])):
                for z in actual_current_income_items_path[x][y]:
                    actual_current_income_items.append(z.text)
        for x in range(len(converted_current_income_items_path)):
            for y in range(len(converted_current_income_items_path[x])):
                for z in converted_current_income_items_path[x][y]:
                    converted_current_income_items.append(z.text)

        actual_current_income_items.sort()
        converted_current_income_items.sort()
        self.assertEqual(converted_current_income_items,actual_current_income_items)

    def test_parties_roles_borrower_borrowerDeclarations(self):
        actual_declarations_path = self.actual_roles_path[0][0][2][0]
        converted_declarations_path = self.converted_roles_path[0][0][2][0]
        actual_declarations = [x.text.strip() for x in actual_declarations_path]
        converted_declarations = [x.text.strip() for x in converted_declarations_path]
        actual_declarations.pop()
        converted_declarations.pop()
        actual_declarations.append(actual_declarations_path.find(f'{self.leadingStr}EXTENSION')[0][0][0].text)
        converted_declarations.append(converted_declarations_path.find(f'{self.leadingStr}EXTENSION')[0][0][0].text)
        actual_declarations.sort()
        converted_declarations.sort()
        self.assertEqual(converted_declarations,actual_declarations)




if __name__ == '__main__':
    unittest.main()
