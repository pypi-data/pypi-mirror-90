# GO GO MEMORI2 
### Here it is the module python 'Freya'.
Freya is a Fremework <3, and this github is the python code.

# Start (Commands CLI). 🚀
With Freya get light curve data is more simple.
Have option by CLI 'freya-admin', the options are:
  
  * Creates new catalog who module inside Freya, where name is the name of catalog what choose and source
  is where it comes from (available options: api,db).
  ```
  freya-admin --newcatalog <name> <source>
  ```
  * Creates new api called FreyaAPI in path with call freya-admin, this opcion create a new flask application with
  all rutes necessaries.
  ```
  freya-admin --newapi
  ```
  * Add new resource in FreyaAPI, but first need whit catalog exist in Freya or local folder and the call --addresource
  inside the folder FreyaAPI.
  ```
  freya-admin --addresource <name> 
  ```
  * And want creates new catalog who local module, can use --newcataloglocal.
  where name is the name of catalog what choose and source is where it comes from (available options: api,db).
  ```
  freya-admin --newcataloglocal <name> <source>

  # then install module
    pip install .
  ```
* Important: the name register with in capital letters, but you can use lowercase name.
# Install Freya. 🔧

```
pip install Freya_alerce

#or clone repository and 

pip install . 

```
## Add new catalogs in Freya or local. 🔧
* If you want add modules catalogs inside Freya use for example:
```
freya-admin --newcatalog ztf api

```
* If you want use local module:
```
# Inside local folder catalogs
freya-admin --newcataloglocal ztf_local api

# then use

pip install .

```
* If you download any catalog for the github or other site you can install in environment python.
```
pip install .
```

Independet how add catalog the next step is to connect catalog with Freya (if not completed before),
for this need completed fourt generic methods.
```
Inside folder new catalog find the following files
- configure.py
- methods.py 
- connect.py (if source is 'db') 

now inside 'configure.py' it find 

  - def get_lc_deg_all(ra,dec,radius,format)

  - def get_lc_hms_all(hms,radius,format)

  - def get_lc_deg_nearest(ra,dec,radius,format)

  - def get_lc_hms_nearest(hms,radius,format)

Need to be completed such that
    - ef get_lc_deg_all(ra,dec,radius,format)
        return all light curves data in csv/votable in an 
        area described in degrees with specific radius.

    - def get_lc_hms_all(hms,radius,format)
        return all light curves data in csv/votable in an 
        area described in hh:mm:ss with specific radius.

    - def get_lc_deg_nearest(ra,dec,radius,format)
        return the light curve data from objecte most close to 
        area described in degrees with specific radius, the data 
        return in csv/votable.

    - def get_lc_hms_nearest(hms,radius,format)
        return the light curve data from objecte most close to 
        area described in hh:mm:ss with specific radius, the data 
        return in csv/votable.

Opcional you can use 'methods.py' for not overburden 'configure.py' but yo can only write in 'configure.py'
```
* For example, ztf is default catalog inside in Freya. 

'~/Freya/catalogs/ztf/configure.py'
```python

from Freya.catalogs.ztf.methods import Methods_ztf as mztf

class Configure_ztf():

    def __init__(self,**kwagrs):
        self.ra = kwagrs.get('ra')
        self.dec = kwagrs.get('dec')
        self.hms = kwagrs.get('hms')
        self.radius = kwagrs.get('radius')
        self.format = kwagrs.get('format')

    def get_lc_deg_all(self):
        data_return = mztf(ra=self.ra,dec=self.dec,radius=self.radius,format=self.format,nearest=False).zftcurves() 
        return data_return

    def get_lc_hms_all(self):
        data_return = mztf(hms=self.hms,radius=self.radius,format=self.format,nearest=False).zftcurves() 
        return data_return

    def get_lc_deg_nearest(self):
        data_return = mztf(ra=self.ra,dec=self.dec,radius=self.radius,format=self.format,nearest=True).zftcurves() 
        return data_return

    def get_lc_hms_nearest(self):
        data_return = mztf(hms=self.hms,radius=self.radius,format=self.format,nearest=True).zftcurves() 
        return data_return

```
'~/Freya/catalogs/ztf/methods.py'
```python

import requests
import io
from Freya.core import utils as u

import pandas
from astropy.io import ascii
from astropy.coordinates import SkyCoord
from astropy import units as u

class Methods_ztf():

    def __init__(self,**kwagrs):
        self.ra = kwagrs.get('ra')
        self.dec = kwagrs.get('dec')
        self.hms = kwagrs.get('hms')
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

    def zftcurves(self):
        """ Get light curves of ztf objects 
        Parameters
        ----------
        """
        baseurl="https://irsa.ipac.caltech.edu/cgi-bin/ZTF/nph_light_curves"
        data = {}
        data['POS']=f'CIRCLE {self.ra} {self.dec} {self.radius}'
        data['FORMAT'] = self.format
        result = requests.get(baseurl,params=data)
        ztfdic = ''
        if result.status_code != 200: 
            ztfdic = result.status_code 
            return ztfdic
        if self.format == 'csv':
            return self.csv_format(result)
```

And if you use catalog with source data base, need complete 'connect.py'
```
# Inside file connect.py
 - user
 - password
 - host
 - port
 - database
```
## Catalogs Default 📖 

### ZTF ()
```
Return:  oid :  Object ID. 
         expid : Exposure ID.
         hjd : Heliocentric Julian Date of the midpoint of the exposure (using the mean ra and dec of the input catalog).
         mjd : Modified Julian Date of the start of the exposure.
         mag :  Magnitude.
         magerr : Uncertainty in mag measurement. Includes correction to conform to photometric repeatability RMS derived from "non-variable" population.
         catflags : Catalog flags for source from PSF-fitting catalog.
         filtercode : Filter code (abbreviated name).
         ra :  Right Ascension of source.
         dec : Declination of source.
         chi : Chi-squared of source.
         sharp : Sharpness of source.
         filefracday : Exposure file timestamp. with decimal representation YYYYMMDDdddddd: year. month. day. and fractional day.
         field :  Field ID.
         ccdid : CCD number (1..16).
         qid : Quadrant ID (1..4).
         limitmag : Approximate 5-sigma limiting magnitude corresponding to epoch- based PSF-fit catalog.
         magzp : Magnitude zeropoint from photometric calibration.
         magzprms : RMS deviation in magnitude zeropoint.
         clrcoeff : Color coefficient from linear fit.
         clrcounc : Color coefficient uncertainty from linear fit.
         exptime : Exposure time from scheduler.
         airmass : Airmass at approximately the center of the focal plane at time of exposure.
         programid : Program ID.
```
### PS1 ()
```
Return : objID : Unique object identifier. 
         detectID : Unique detection identifier.,
         filterID : Filter identifier. Details in the Filter table.
         obsTime : Modified Julian Date at the midpoint of the observation.
         ra : Right ascension.
         dec : Declination.
         psfFlux : Flux from PSF fit.
         psfFluxErr :  Error on flux from PSF fit.
         psfMajorFWHM : PSF major axis FWHM.
         psfMinorFWHM : PSF minor axis FWHM.
         psfQfPerfect : PSF weighted fraction of pixels totally unmasked.
         apFlux : Flux in seeing-dependent aperture.
         apFluxErr : Error on flux in seeing-dependent aperture.
         infoFlag : Information flag bitmask indicating details of the photometry. Values listed in DetectionFlags.
         infoFlag2 : Information flag bitmask indicating details of the photometry. Values listed in DetectionFlags2. 
         infoFlag3 : Information flag bitmask indicating details of the photometry. Values listed in DetectionFlags3.
```

* objID --> oid
* obsTime --> mjd

## New FreyaAPI
Other application of Freya is quick creation for the API used flask:
```
# In any directory in your system
freya-admin --newapi

```
In folder where is called create new flask application, it contains the
necessary routes generic that you only call and not modified, but first you need
add resources(catalogs) with :

```
# Inside folder FreyaAPI

freya-admin --addresource ztf
freya-admin --addresource ztf_local

```
Now you can run the FreyaAPI using : 

# Start (Who use)🚀
How to use the Freya and FreyaAPI.
First you look the complete demo (link al git que tenga todo)

## How use the rute FreyaAPI
The rutes in FreyaAPI are get methods and have four rutes.
```
 # Get light curves of objects with area in degrees.
 args : - catalogs: string
        - ra: float (degrees) 
        - dec: float (degrees)
        - radius: float (arcsec)
        - format: csv,votable
 Example:
  http://localhost/get_data/lc_degree?catalogs=ztf&ra=139.33444972&dec=68.6350604&radius=0.0002777&format=csv
 
 # Get light curve of object most close to area in degrees.
 args : - catalogs: string
        - ra: float (degrees) 
        - dec: float (degrees)
        - radius: float (arcsec)
        - format: csv,votable
 Example:
  http://localhost/get_data/lc_degree_nearest?catalogs=ztf&ra=139.33444972&dec=68.6350604&radius=0.0002777&format=votable   
```
```
 # Get light curves of objects with area in hh:mm:ss.
 args : - catalogs: string
        - hms: string
        - radius: float (arcsec)
        - format: csv,votable
 Example:
    http://localhost/get_data/lc_hms?catalogs=ztf&hms=%279h17m20.26793280000689s%20+4h34m32.414496000003936s%27&radius=0.0002777&format=csv
 
 # Get light curve of object most close to area in hh:mm:ss.
 args : - catalogs: string
        - hms: string
        - radius: float (arcsec)
        - format: csv,votable
 Example:
   http://localhost/get_data/lc_hms_nearest?catalogs=ztf&hms=%279h17m20.26793280000689s%20+4h34m32.414496000003936s%27&radius=0.0002777&format=votable 
```
## How use a only Freya
If you want use Freya but without installing, you can use the method 'GetData'.
```
from Freya.catalogs.core import GetData

data_all_deg = GetData(catalog='ztf',ra=139.33444972,dec=68.6350604,radius=0.0002777,format='csv').get_lc_deg_all()
data_one_deg = GetData(catalog='ztf',ra=139.33444972,dec=68.6350604,radius=0.0002777,format='csv').get_lc_deg_nearest()
data_all_hms = GetData(catalog='ztf',hms='9h17m20.26793280000689s +4h34m32.414496000003936s',radius=0.0002777,format='votable').get_lc_hms_all()
data_one_hms = GetData(catalog='ztf',hms='9h17m20.26793280000689s +4h34m32.414496000003936s',radius=0.0002777,format='votable').get_lc_hms_nearest()
```
# Build with 🛠️
* Python : 3.9
###
Jonimott de Malpais - [fernandezeric](https://github.com/fernandezeric)
