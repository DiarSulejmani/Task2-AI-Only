from pydantic import BaseModel, EmailStr
class Foo(BaseModel):
    email: EmailStr

print('Ok')