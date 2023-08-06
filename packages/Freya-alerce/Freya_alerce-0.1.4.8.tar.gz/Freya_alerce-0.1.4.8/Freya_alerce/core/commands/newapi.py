from Freya_alerce.core.base import Base

"""
Created new FreyaAPI

Parameters
--------------------------------------
path : (string) path where created FreyaAPI.
"""
class NewAPI(Base):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        super().create_new_api()