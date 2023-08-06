import requests
import io
from Freya_alerce.core import utils

from astropy.io import ascii
from astropy.table import Table,vstack
from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.io.votable import parse,parse_single_table, writeto

"""
MethodsPS1, you can use this method if you do not want overburden configure.py, especially want to use module class to get data, you can replace all script.
"""
class MethodsPS1():

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

    def ps1cone(self, format='csv',baseurl="https://catalogs.mast.stsci.edu/api/v0.1/panstarrs", **kw):
            #table="mean",release="dr1",format="csv",columns=None,
        """Do a cone search of the PS1 catalog
        Parameters
        ----------
        """
        data = kw.copy()
        data['ra'] = self.ra
        data['dec'] = self.dec
        data['radius'] = self.radius
        #data['format'] = self.format
        return self.ps1search(format=format,baseurl=baseurl, **data)

    #https://ps1images.stsci.edu/ps1_dr2_api.html
    def ps1search(self,format='csv',table="mean",release="dr1",columns=None,baseurl="https://catalogs.mast.stsci.edu/api/v0.1/panstarrs",**kw):
        #table="mean",release="dr1",columns=None,
        """Do a general search of the PS1 catalog (possibly without ra/dec/radius)
        
        Parameters
        ----------
        """
        data = kw.copy()
        url = f"{baseurl}/{release}/{table}.{format}"
        data['columns'] = '[{}]'.format(','.join(columns))
        r = requests.get(url, params=data)
        r.raise_for_status()
        if self.format == "json":
            return r.json()
        else:
            return r.text

    def ps1ids(self):
        """Get ids (ps1 id) of objects in a radius with respect to ra and dec
        Parameters
        ----------
        """
        constraints = {'nDetections.gt':1}
        columns = ['objID','raMean','decMean']
        results = self.ps1cone(release='dr2',columns=columns,**constraints)

        try:
            results = ascii.read(results)
        except:
            return []

        if self.nearest is True:
            angle = []
            c1 = SkyCoord(ra=self.ra,dec=self.dec,unit=u.degree)
            for re in results:
                c2 = SkyCoord(ra=re['raMean'],dec=re['decMean'],unit=u.degree)
                angle.append(c1.separation(c2))
            minps1 = angle.index(min(angle))
            temp = []
            temp.append(results[minps1]['objID'])
            return temp

        else :
            return results['objID']


    def ps1curves(self):
        """Get light curves of objects in specific radio with respect ra and dec, and possible return the object most nearest to radio
        Parameters
        ----------
        """
        ps1dic = ''
        first = True
        ids = self.ps1ids()
        if not any(ids):
            ps1dic = 'not found' # not object find
            return ps1dic

        dcolumns = ("""objID, detectID,filterID,obsTime,ra,dec,psfFlux,psfFluxErr,psfMajorFWHM,psfMinorFWHM,
                    psfQfPerfect,apFlux,apFluxErr,infoFlag,infoFlag2,infoFlag3""").split(',') 
        dcolumns = [x.strip() for x in dcolumns]
        dcolumns = [x for x in dcolumns if x and not x.startswith('#')]

        #split ids in dict
        for id in ids:
            dconstraints = {'objID': id}
            dresults = self.ps1search(format =self.format,table='detection',release='dr2',columns=dcolumns,**dconstraints)
            if(self.format == 'csv'):
                if first :
                    dresults_ = ascii.read(dresults)
                    first = False
                #
                else :
                    dresults_ = vstack([dresults_,ascii.read(dresults)])
                # 
            elif(self.format == 'votable'):
                votable = dresults.encode(encoding='UTF-8')
                bio = io.BytesIO(votable)
                votable = parse(bio)
                table = parse_single_table(bio).to_table()
                if first :
                    dresults_ = table
                    first = False

                else :
                    dresults_ = vstack([dresults_,table])
                               
        
        #remane colmun objID -> oid and obsTime -> mjd
        if (self.format == 'csv'): 
            dresults_.rename_column('objID', 'oid')
            dresults_.rename_column('obsTime', 'mjd')
            buf = io.StringIO()
            ascii.write(dresults_,buf,format='csv')
            ps1dic =  buf.getvalue()
            return ps1dic
            
        elif (self.format == 'votable'):
            dresults_.rename_column('objID', 'oid')
            dresults_.rename_column('obsTime', 'mjd')
            buf = io.BytesIO()
            writeto(dresults_,buf)
            ps1dic = (buf.getvalue().decode("utf-8"))
            return ps1dic




        