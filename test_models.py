from backend import models
from backend.database import Base

print('Tables:', Base.metadata.tables.keys())