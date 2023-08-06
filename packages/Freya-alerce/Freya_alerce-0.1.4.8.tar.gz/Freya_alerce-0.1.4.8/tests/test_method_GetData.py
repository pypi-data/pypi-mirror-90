from unittest import TestCase, mock
from Freya_alerce.catalogs.core import GetData

class TestMethodGetData(TestCase):
    
    def setUp(self):
        self.test_get_data_degree = GetData(catalog='test1',ra=139.33444972,dec=68.6350604)
        self.test_get_data_hms = GetData(catalog='test2',hms = '9h17m20.26793280000689s +4h34m32.414496000003936s')


    @mock.patch.object(GetData, "generic_call_data")
    def test(self,mock1):
        str_test = 'Ligth Curve Data'
        mock1.return_value = str_test

        self.assertEqual(self.test_get_data_degree.get_lc_deg_all(), str_test)
        self.assertEqual(self.test_get_data_degree.get_lc_deg_nearest(), str_test)
        self.assertEqual(self.test_get_data_degree.get_lc_hms_all(), str_test)
        self.assertEqual(self.test_get_data_degree.get_lc_hms_nearest(), str_test)

        self.assertEqual(self.test_get_data_hms.get_lc_deg_all(), str_test)
        self.assertEqual(self.test_get_data_hms.get_lc_deg_nearest(), str_test)
        self.assertEqual(self.test_get_data_hms.get_lc_hms_all(), str_test)
        self.assertEqual(self.test_get_data_hms.get_lc_hms_nearest(), str_test)

        
if __name__ == '__main__':
    unittest.main() 

