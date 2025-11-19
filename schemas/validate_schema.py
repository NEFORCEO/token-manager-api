from pydantic import BaseModel, Field

class Valid(BaseModel):
    token: str = Field(min_length=17)