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

    def test_parties(self):
        actual_individual_path = self.actual_deal_path[4][0][0]
        converted_individual_path = self.converted_deal_path[4][0][0]
        self.assertEqual(len(converted_individual_path),len(actual_individual_path))
        self.assertEqual(converted_individual_path.tag,actual_individual_path.tag)
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

        self.assertEqual(converted_contact_points,actual_contact_points)





if __name__ == '__main__':
    unittest.main()
