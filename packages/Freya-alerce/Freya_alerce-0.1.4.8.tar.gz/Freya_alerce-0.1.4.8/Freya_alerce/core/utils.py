
from astropy.coordinates import SkyCoord

"""
This class represent the generic methods
"""
class Utils:

    def deg_to_hms(self):
        """
        """
        pass

    def hms_to_deg(self,hms):
        """
        """
        coord = SkyCoord(hms,frame='icrs') #transform coord
        ra = coord.ra.degree
        dec = coord.dec.degree
        return ra,dec

    def nearest(self):
        pass