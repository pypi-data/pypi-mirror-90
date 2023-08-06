import tempfile
import shutil
import zipfile
import unittest

from Freya_alerce.core.base import Base
import Freya_alerce.files.list_file as files_

class TestCreateApi(unittest.TestCase):
    
    def setUp(self):
        self.temp_FreyaApi = tempfile.TemporaryDirectory()

    def test(self):
        path_template_api = Base().path_file_template_new_api()
        extract_zip = zipfile.ZipFile(path_template_api)
        extract_zip.extractall(self.temp_FreyaApi.name)
        extract_zip.close()

    def tearDown(self):
        self.temp_FreyaApi.cleanup()

if __name__ == '__main__':
    unittest.main() 