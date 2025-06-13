from pydantic import constr

a = constr(regex=r'[^@]+@[^@]+')
print(a)