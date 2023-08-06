import os
import sys
import subprocess
import tempfile
import shutil
import Freya_alerce.catalogs # __path__
import Freya_alerce.files.list_file as files_
import zipfile #read zip files
from Freya_alerce.files.verify_file import Verify


"""
Base class to command line Freya, contains method for add new catalog inside Freya or in local folder, 
created new local folder, new api (FreyaAPI), and add resources in FreyaAPI.
"""
class Base():
    """
    Parameters
    --------------------------------------
    name : (string) name with add catalog inside Freya or in local folder
            and is the same name with add resource in FreyaAPI
    source : (string) origin source catalog [api,db]

    path : (string) path where created FreyaAPI, local folder for catalogs and
            add resources in FreyaAPI.
    """

    def __init__(self,**kwargs):
        self.name = kwargs.get('name')
        if self.name:
            #self.name = self.name.replace(self.name[0],self.name[0].upper(),1)
            self.name = self.name.upper()
        self.source = kwargs.get('source')
        self.path = kwargs.get('path')

    def path_files_template_from(self):
        """
        Select path of *.zip to extract, depend the source catalog.
        """
        if self.source == 'api':
            return os.path.join(Freya_alerce.files.__path__[0],'file_templates','fromapi.zip')
        else :
            return os.path.join(Freya_alerce.files.__path__[0],'file_templates','fromdb.zip')
    
    def path_file_template_new_api(self):
        """
        Get the path of FreyaAPI generic data for extracted.
        """
        return os.path.join(Freya_alerce.files.__path__[0],'file_templates','newapi.zip')
    
    def path_file_template_resource(self):
        """
        Get the path of FreyaAPI resource generic data for extracted.
        """
        return os.path.join(Freya_alerce.files.__path__[0],'file_templates','newresource.zip')
    
    def create_module_catalog(self):
        """
        Create new catalog module inside Freya,
        first verify if source catalog is valid, 
        second verify the catalog already exist then get path
        for new module catalog and path template data,
        finaly try create the new module folder and extract the data.
        """
        
        #self.name= self.name.upper()
        if Verify().verify_source(self.source):
            raise TypeError (f'The source not is valid')

        if Verify().verify_catalog_inside(self.name) or Verify().verify_catalog_local(self.name):  
            raise TypeError ('catalog already created')
        
        dir_catalogs = Freya_alerce.catalogs.__path__[0]
        path_new_catalog = os.path.join(dir_catalogs,self.name)
        path_tample_files_ = self.path_files_template_from()

        try: 
            with tempfile.TemporaryDirectory() as tmpdir:
                #print('created temporary directory', tmpdirname)
                extract_zip = zipfile.ZipFile(path_tample_files_)
                if self.source == 'api':
                    listOfFileNames = ['configure.py','methods.py','__init__.py']
                elif self.source == 'db':
                    listOfFileNames = ['configure.py','methods.py','connect.py','__init__.py']
                for fileName in listOfFileNames:
                    extract_zip.extract(fileName, tmpdir)
                extract_zip.close()
                # Replace word 'NAME' from the name catalog
                if self.source == 'api':
                    list_path = [os.path.join(tmpdir,'configure.py'),os.path.join(tmpdir,'methods.py')]
                elif self.source == 'db':
                    list_path = [os.path.join(tmpdir,'configure.py'),os.path.join(tmpdir,'methods.py'),os.path.join(tmpdir,'connect.py')]
                files_.Files(list_path,'NAME',self.name).replace_in_files()
                shutil.copytree(tmpdir,path_new_catalog)
        except OSError as error:
            print(error)  
    
    def create_module_catalog_local(self):
        """
        Create new local catalog module ,
        first verify if source catalog is valid, 
        second verify the catalog already exist then get path
        for new module catalog and path template data,
        finaly try create the new module folder and extract the data.

        The catalog create in path with call the freya-admin.
        Need call inside local folder to take Freya.
        """
        if Verify().verify_source(self.source):
            raise TypeError (f'The source {self.source} not is valid')

        if Verify().verify_catalog_inside(self.name) or Verify().verify_catalog_local(self.name):  
            raise TypeError ('catalog already created')

        path_new_catalog = os.path.join(self.path,f'Local{self.name}')
        path_tample_files_ = self.path_files_template_from()

        try: 
            with tempfile.TemporaryDirectory() as tmpdir:
                #print('created temporary directory', tmpdirname)
                extract_zip = zipfile.ZipFile(path_tample_files_)
                extract_zip.extract('setup.py', tmpdir)
                path_new_catalog_ = os.path.join(tmpdir,f'{self.name}')
                os.mkdir(path_new_catalog_)
                #
                if self.source == 'api':
                    listOfFileNames = ['configure.py','methods.py','__init__.py']
                elif self.source == 'db':
                    listOfFileNames = ['configure.py','methods.py','connect.py','__init__.py']
                for fileName in listOfFileNames:
                    extract_zip.extract(fileName, path_new_catalog_)
                extract_zip.close()
                # Replace word 'NAME' from the name catalog
                if self.source == 'api':
                    list_path = [os.path.join(path_new_catalog_,'configure.py'),os.path.join(path_new_catalog_,'methods.py')]
                elif self.source == 'db':
                    list_path = [os.path.join(path_new_catalog_,'configure.py'),os.path.join(path_new_catalog_,'methods.py'),os.path.join(path_new_catalog_,'connect.py')]
                #
                files_.Files(list_path,'Freya_alerce.catalogs.','').replace_in_files()
                files_.Files(list_path,'NAME',self.name).replace_in_files()
                #
                list_path_ = [os.path.join(tmpdir,'setup.py')]
                files_.Files(list_path_,'NAME',self.name).replace_in_files()
                # 
                shutil.copytree(tmpdir,path_new_catalog)
        except OSError as error:
            print(error)   

    def create_new_api(self):
        """
        Create a new FreyaAPI, the new api created in path
        with call the freya-admin --newapi
        """
        # Get the path template data for FreyaAPI
        path_template_api = self.path_file_template_new_api()
        # Get the path when create new api
        path_new_api =  os.path.join(self.path,'FreyaAPI')
        # Install Flask - Astropy - Flask-restplus
        subprocess.check_call([sys.executable, '-m','pip', 'install','-r',os.path.join(os.path.dirname(__file__),'requirementsAPI.txt')])
        # Extract template data
        try: 
            with tempfile.TemporaryDirectory() as tmpdir:
                #print('created temporary directory', tmpdirname)
                extract_zip = zipfile.ZipFile(path_template_api)
                extract_zip.extractall(tmpdir)
                extract_zip.close()
                shutil.copytree(tmpdir,path_new_api)
        except OSError as error:
            print(error)    
    
    def create_new_resource(self):
        """
        Add resource to FreyaAPI, first verify the catalog exist inside Freya 
        or in the local catalogs folder.
        """
        # Verify 
        if not Verify().verify_catalog_inside(self.name) and not Verify().verify_catalog_local(self.name) and not Verify().verify_catalog_local_(self.name):
            raise TypeError ('first created catalog inside Freya or local ')
        
        # Get path to template files
        path_template_resource = self.path_file_template_resource()
        # New path 
        path_api =  self.path
        # 
        path_new_resource = os.path.join(path_api,f'app/resources/{self.name}_resource')

        try: 
            with tempfile.TemporaryDirectory() as tmpdir:
                #print('created temporary directory', tmpdirname)
                extract_zip = zipfile.ZipFile(path_template_resource)
                extract_zip.extractall(tmpdir)
                extract_zip.close()
                list_path = [os.path.join(tmpdir,'resource.py')]
                files_.Files(list_path,'NAME',self.name).replace_in_files()
                shutil.copytree(tmpdir,path_new_resource)
        except OSError as error:
            print(error)    
        


