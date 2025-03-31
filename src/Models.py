from typing import List

from pydantic import BaseModel

# HERE WILL BE ALL REQUEST-RESPONSE MODELS

class RAGResponse(BaseModel):
    user_id:int
    response:str

class RAGRequest(BaseModel):
    user_id:int
    query:str

class RAGAddSourcesRequest(BaseModel):
    user_id:int
    sources:List[str]

