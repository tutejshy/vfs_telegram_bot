from pydantic.main import BaseModel


class Account(BaseModel):
    
    class Config:
        orm_mode = True
