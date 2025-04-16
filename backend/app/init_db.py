from .database import engine
from . import models

# Create the tables
models.Base.metadata.create_all(bind=engine)
