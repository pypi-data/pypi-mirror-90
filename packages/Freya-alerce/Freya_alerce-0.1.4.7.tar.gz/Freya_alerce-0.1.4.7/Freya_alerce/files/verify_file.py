
import Freya_alerce.catalogs # __path__ # dir modules
import os
import importlib

"""
Class to verify if exist catalog inside Freya or in local folder, and if source is permitted.
"""
class Verify():

    """
    Verify name catalog already exist inside Freya, if exist return true.
    """
    def verify_catalog_inside(self,name):
        self.name = name
        dir_catalogs = Freya_alerce.catalogs.__path__[0]
        if self.name  in os.listdir(dir_catalogs) :
             return True 
        return False

    """
    Verify name catalog already exist in local folder fromc catalogs,
    frist try import the local folder and then verify if exist name catalog.
    Return True if name catalog exist and return false if not exist local folfer
    or not exist name catalog.
    """
    def verify_catalog_local(self,name):
        self.name = name
        try :
            mod = importlib.import_module('LocalCatalogs')
            dir_catalogs = mod.__path__[0]
            if self.name  in os.listdir(dir_catalogs) :
                return True 
            return False
        except:
            return False

    """
    Verify if catalogue path exist in any place.
    """
    def verify_catalog_local_(self,name):
        self.name = name
        try:
            mod = importlib.import_module(f'{self.name}')
            return True
        except:
            return False
    
    """
    Verify if source of catalog is permitted who source.
    Return True if source not is valid.
    """  
    def verify_source(self,source):
        self.source = source
        if self.source not in ['api','db']:
            return True
        return False
