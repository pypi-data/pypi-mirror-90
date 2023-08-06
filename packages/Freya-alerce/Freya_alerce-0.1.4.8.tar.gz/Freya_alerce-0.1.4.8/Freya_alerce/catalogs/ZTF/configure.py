"""
configure.py is the most important file in Freya, this file is called for 
Freya’s core and FreyaAPI’s resources, is the only file you need to modify 
in principle. You need to complete the following methods. When using Freya’s 
method getData, you use this class for calls and depent what method call you 
need use ra and dec or hms, so that's why kwargs is used.
"""

from Freya_alerce.catalogs.ZTF.methods import MethodsZTF as mztf
from Freya_alerce.core.utils import Utils

class ConfigureZTF():
    """
    Parameters:
    ------------
    ra : (float) Right ascension
    dec :  (float) Declination
    hms : (string) HH:MM:SS
    radius: (float) Search radius
    format: (string) csv or votable
    """
    def __init__(self,**kwagrs):
        self.ra = kwagrs.get('ra')
        self.dec = kwagrs.get('dec')
        self.hms = kwagrs.get('hms')
        self.radius = kwagrs.get('radius')
        self.format = kwagrs.get('format')

    """
    Need return light curves data from objects inside the area delimited for ra,dec,radius. 
    The format return is the specific ‘format’ when called in the class.
    """
    def get_lc_deg_all(self):
        """
        Return all ligth curves data inside degree area from ZTF catalog.
        """
        data_return = mztf(ra=self.ra,dec=self.dec,radius=self.radius,format=self.format,nearest=False).zftcurves() 
        return data_return
    """
    Need return light curves data from objects inside the area delimited for hh:mm:ss,radius. 
    The format return is the specific ‘format’ when called in the class.
    """
    def get_lc_hms_all(self):
        """
        Return all ligth curves data inside hh:mm:ss area from ZTF catalog.
        """
        ra_,dec_ = Utils().hms_to_deg(self.hms)
        data_return = mztf(ra=ra_,dec=dec_,radius=self.radius,format=self.format,nearest=False).zftcurves() 
        return data_return
    """
    Need return light curve data from the object most nearest inside the area delimited for ra,dec,radius. 
    The format return is the specific ‘format’ when called in the class.
    """
    def get_lc_deg_nearest(self):
        """
        Return the ligth curve data most close to point in degree area from ZTF catalog.
        """
        data_return = mztf(ra=self.ra,dec=self.dec,radius=self.radius,format=self.format,nearest=True).zftcurves() 
        return data_return
    """
    Need return light curve data from the object most nearest inside the area delimited for hh:mm:ss, radius. 
    The format return is the specific ‘format’ when called in the class.
    """
    def get_lc_hms_nearest(self):
        """
        Return the ligth curve data most close to point in hh:mm:ss area from ZTF catalog.
        """
        ra_,dec_ = Utils().hms_to_deg(self.hms)
        data_return = mztf(ra=ra_,dec=dec_,radius=self.radius,format=self.format,nearest=True).zftcurves() 
        return data_return