import tempfile
import shutil
import zipfile
import os
import unittest

from Freya_alerce.core.base import Base
import Freya_alerce.files.list_file as files_

class TestCreateModuleLocalApi(unittest.TestCase):
    

    def setUp(self):
        self.tmp_test = tempfile.TemporaryDirectory()

    def test(self):
        path_template_api = Base(source='api').path_files_template_from()
        extract_zip = zipfile.ZipFile(path_template_api)

        extract_zip.extract('setup.py', self.tmp_test.name)
        path_new_catalog_ = os.path.join(self.tmp_test.name,'Test')
        os.mkdir(path_new_catalog_)
        listOfFileNames = ['configure.py','methods.py','__init__.py']

        for fileName in listOfFileNames:
            extract_zip.extract(fileName, path_new_catalog_)

        extract_zip.close()

        list_path = [os.path.join(path_new_catalog_,'configure.py'),os.path.join(path_new_catalog_,'methods.py')]
        files_.Files(list_path,'NAME','test').replace_in_files()

        files_.Files(list_path,'Freya_alerce.catalogs.','').replace_in_files()
        files_.Files(list_path,'NAME','Test_').replace_in_files()
        #
        list_path_ = [os.path.join( self.tmp_test.name,'setup.py')]
        files_.Files(list_path_,'NAME','Test_').replace_in_files()

    def tearDown(self):
        self.tmp_test.cleanup()

if __name__ == '__main__':
    unittest.main() 