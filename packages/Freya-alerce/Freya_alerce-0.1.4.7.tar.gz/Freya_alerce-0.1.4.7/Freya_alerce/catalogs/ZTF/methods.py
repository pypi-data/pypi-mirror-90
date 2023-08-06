import requests
import io
from Freya_alerce.core import utils as u

import pandas
from astropy.io import ascii
from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.io.votable import parse,parse_single_table,from_table, writeto

"""
MethodsZTF, you can use this method if you do not want overburden configure.py, especially want to use module class to get data, you can replace all script.
"""
class MethodsZTF():

    """
    Parameters
    ----------
    ra : (float) Right ascension
    dec :  (float) Declination
    radius: (float) Search radius
    format: (string) csv or votable
    nearest: (bool) Flag to indicate if you get all or one light curve from the object.
    """
    def __init__(self,**kwagrs):
        self.ra = kwagrs.get('ra')
        self.dec = kwagrs.get('dec')
        self.radius = kwagrs.get('radius')
        self.format = kwagrs.get('format')
        self.nearest = kwagrs.get('nearest')

    def id_nearest (self,results):
        """ Get object id most closet to ra dec use a min angle
        Parameters
        ----------
        """
        angle = []
        c1 = SkyCoord(ra=self.ra,dec=self.dec,unit=u.degree)
        for group in results.groups:
            c2 = SkyCoord(group['ra'][0],group['dec'][0],unit=u.degree)
            angle.append(c1.separation(c2))
        return angle.index(min(angle))

    def csv_format(self,result):
        ztfdic = ''
        result_ = ascii.read(result.text)
        if len(result_) <= 0:
            ztfdic = 'light curve not found' 
            return ztfdic

        #the most close object to radius
        if self.nearest is True:
            
            result_ = result_.group_by('oid')
            minztf = self.id_nearest(result_)
            
            buf = io.StringIO()
            ascii.write(result_.groups[minztf],buf,format='csv')
            ztfdic =  buf.getvalue()
            return ztfdic

        # all objects in radius
        else:
            ztfdic = result.text
            return ztfdic

    def votable_format(self,result):
        ztfdic = ''
        votable = result.text.encode(encoding='UTF-8')
        bio = io.BytesIO(votable)
        votable = parse(bio)
        table = parse_single_table(bio).to_table()

        if len(table) <= 0:
            ztfdic['0'] = 'not found' 
            return ztfdic #'not found'0


        #the most close object to radius
        if self.nearest is True:
            tablas = table.group_by('oid')
            minztf = self.id_nearest(tablas)
            buf = io.BytesIO()
            votable = from_table(tablas.groups[minztf])
            writeto(votable,buf)
            ztfdic = (buf.getvalue().decode("utf-8"))
            return ztfdic
        # all objects in radius
        else :
            ztfdic = result.text
            return ztfdic

    def zftcurves(self):
        """ Get light curves of ztf objects 
        Parameters
        ----------
        """
        baseurl="https://irsa.ipac.caltech.edu/cgi-bin/ZTF/nph_light_curves"
        data = {}
        data['POS']=f'CIRCLE {self.ra} {self.dec} {self.radius}'
        #data['BANDNAME']='r'
        data['FORMAT'] = self.format
        result = requests.get(baseurl,params=data)
        ztfdic = ''
        #self.csv_format(result)
        #return result
        if result.status_code != 200: 
            ztfdic = result.status_code 
            return ztfdic
        #if select csv 
        if self.format == 'csv':
            return self.csv_format(result)
        # if select VOTable 
        elif self.format == 'votable':
            return self.votable_format(result)