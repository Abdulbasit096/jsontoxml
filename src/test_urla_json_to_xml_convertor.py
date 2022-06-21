import unittest
import xml.etree.ElementTree as ET
import urla_json_to_xml_convertor as jtox
from config import get_project_root
import json

class MyTestCase(unittest.TestCase):



    @classmethod
    def setUpClass(cls):
        cls.case_id = jtox.case_id
        cls.convertedXml = open(f'{get_project_root()}/test_resources/{cls.case_id}.xml','r')
        cls.convertedRoot = ET.parse(cls.convertedXml).getroot()
        cls.actualXml = open(f'{get_project_root()}/test_resources/{cls.case_id}_actual.xml','r')
        cls.actualRoot = ET.parse(cls.actualXml).getroot()


    @classmethod
    def tearDownClass(cls):
        cls.actualXml.close()
        cls.convertedXml.close()

    def test_YesNoToBoolean(self):
        actual_one = jtox.YesNOtoBoolean('Yes')
        expected_one = 'true'
        actual_two = jtox.YesNOtoBoolean('no')
        expected_two = 'false'
        actual_three = jtox.YesNOtoBoolean(None)
        self.assertEqual(expected_one,actual_one)
        self.assertEqual(expected_two,actual_two)
        self.assertIsNone(actual_three)


    def test_checkIfJsonExist(self):
        file = open(f'{get_project_root()}/test_resources/test.json','r')
        data = dict(json.load(file))
        actual = jtox.checkIfJsonExist(data,'name')
        expected = data['name']
        self.assertEqual(expected,actual)
        actual_two = jtox.checkIfJsonExist(data,'age')
        self.assertIsNone(actual_two)
        file.close()


    def test_compare_roots(self):
        jtox.createRoot()
        self.assertEqual(self.convertedRoot.tag,self.actualRoot.tag)

    def test_compare_root_attr(self):
        self.assertEqual(self.convertedRoot.attrib,self.actualRoot.attrib)

    


if __name__ == '__main__':
    unittest.main()
