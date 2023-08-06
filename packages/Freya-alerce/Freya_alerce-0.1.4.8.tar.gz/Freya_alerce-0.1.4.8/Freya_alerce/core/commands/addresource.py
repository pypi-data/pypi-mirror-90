from Freya_alerce.core.base import Base

"""
Add resource to FreyaAPI, need call inside FreyaAPI

Parameters
--------------------------------------
name : (string) name catalogue in Freya what adds resource in FreyaAPI.
"""
class AddResource(Base):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        super().create_new_resource()