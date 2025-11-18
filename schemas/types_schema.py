from pydantic import BaseModel

class Items(BaseModel):
    status_code: int

class CreateTokens(Items):
    token: str 
    
class ValidateTokens(Items):
    status: bool
    
class DeleteTokens(ValidateTokens):
    ...
    
    