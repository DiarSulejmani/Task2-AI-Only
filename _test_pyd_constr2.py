from pydantic import constr, BaseModel
class Foo(BaseModel):
    email: constr(pattern=r"[^@]+@[^@]+\.[^@]+", min_length=3, max_length=320)
print('ok')