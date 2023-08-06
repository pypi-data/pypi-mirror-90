import tempfile
import shutil
import os
import zipfile
import unittest

from Freya_alerce.core.base import Base
import Freya_alerce.files.list_file as files_

class TestAddResource(unittest.TestCase):
    
    def setUp(self):
        self.temp_FreyaAPI = tempfile.TemporaryDirectory()

    def test(self):
        path_template_FreyaApi = Base().path_file_template_new_api()
        extract_zip = zipfile.ZipFile(path_template_FreyaApi)
        extract_zip.extractall(self.temp_FreyaAPI.name)
        extract_zip.close()

        path_new_resource = os.path.join(self.temp_FreyaAPI.name,'resources/Test_resource')
        path_template_resource = Base().path_file_template_resource()
        extract_zip = zipfile.ZipFile(path_template_resource)
        extract_zip.extractall(path_new_resource)
        extract_zip.close()
        list_path = [os.path.join(path_new_resource,'resource.py')]
        files_.Files(list_path,'NAME','Test').replace_in_files()

    def tearDown(self):
        self.temp_FreyaAPI.cleanup()

if __name__ == '__main__':
    unittest.main() 