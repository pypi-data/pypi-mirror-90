from Freya_alerce.core.base import Base

"""
Add new catalogue in local folder.
--------------------------------------

Parameters
name : (string) name with add catalogue in local folder.
source : (string) origin source catalogue [api,db]
"""
class AddCatalogLocal(Base):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        super().create_module_catalog_local()