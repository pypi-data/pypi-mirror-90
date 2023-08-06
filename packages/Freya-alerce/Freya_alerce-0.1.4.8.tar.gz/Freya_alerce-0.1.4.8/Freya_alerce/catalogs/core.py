import os
import importlib
from Freya_alerce.files.verify_file import Verify

"""
Class to get data from module catalog configured in Freya, first check if catalog exist inside Freya
and if not exist try import catalog from local folder. The data get is all ligh curve of object in area use
degrees (ra,dec,radius) or use the format hh:mm:ss (hh:mm:ss,radius).
Other option is get the only light curve of object most close to area selected.
"""
class GetData ():
    """
    Parameters
    -------------------------------------- 
    ra (float): (degrees) Right Ascension
    
    dec (float): (degrees) Declination 

    hms (string): format hh:mm:ss

    radius (float): Search radius
    
    format (string): csv,votable
    """

    def __init__(self,radius=0.0002777,format='csv',**kwargs):
        self.catalog = kwargs.get('catalog').strip().upper()
        #self.catalog = self.catalog.replace(self.catalog[0],self.catalog[0].upper(),1)
        self.ra = kwargs.get('ra')
        self.dec = kwargs.get('dec')
        self.hms = kwargs.get('hms')
        self.radius = radius
        self.format = format

        if self.format not in ['csv','votable']:
             return "inadmissible format in consult data"
    

    def generic_call_data(self,call_method):
        try :
            """
            Search catalog insiede Freya, if not exist search inside local folder.
            """
            if Verify().verify_catalog_inside(self.catalog):
                module = f'Freya_alerce.catalogs.{self.catalog}.configure'
            elif Verify().verify_catalog_local(self.catalog) :
                module = f'LocalCatalogs.{self.catalog}.configure'
            else :
                module = f'{self.catalog}.configure'

            # Import self.catalog
            mod = importlib.import_module(module)
            # Call class
            class_ =  getattr(mod,f'Configure{self.catalog}') 
            # Call method especific of class
            if call_method == 'get_lc_deg_all':
                method_ = class_(ra = self.ra,
                                    dec = self.dec,
                                    radius = self.radius,
                                    format=self.format).get_lc_deg_all()
            elif call_method == 'get_lc_deg_nearest':
                method_ = class_(ra = self.ra,
                                    dec = self.dec,
                                    radius = self.radius,
                                    format=self.format).get_lc_deg_nearest()
            
            elif call_method == 'get_lc_hms_all':
                method_ = class_(hms = self.hms,
                                    radius = self.radius,
                                    format = self.format).get_lc_hms_all()
            
            elif call_method == 'get_lc_hms_nearest':
                method_ = class_(hms = self.hms,
                                    radius = self.radius,
                                    format = self.format).get_lc_hms_nearest()
            return method_
        except :
            print(f'No find the catalog : {self.catalog}')

    def get_lc_deg_all(self):
        """
        Return all light curve object in degrees area.
        """
        return self.generic_call_data('get_lc_deg_all')

    def get_lc_deg_nearest(self):
        """
        Return the light curve most close to degrees area.
        """
        return self.generic_call_data('get_lc_deg_nearest')

    def get_lc_hms_all(self):
        """
        Return all light curve object in hh:mm:ss area.
        """
        return self.generic_call_data('get_lc_hms_all')

    def get_lc_hms_nearest(self):
        """
        Return the light curve most close to hh:mm:ss area.
        """
        return self.generic_call_data('get_lc_hms_nearest')