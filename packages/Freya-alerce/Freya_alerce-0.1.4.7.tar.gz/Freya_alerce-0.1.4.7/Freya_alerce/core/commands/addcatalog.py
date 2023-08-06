from Freya_alerce.core.base import Base

"""
Add new catalogue inside Freya.

Parameters
--------------------------------------
name : (string) name with add catalogue inside Freya
source : (string) origin source catalogue [api,db]
"""
class AddCatalog(Base):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        super().create_module_catalog()