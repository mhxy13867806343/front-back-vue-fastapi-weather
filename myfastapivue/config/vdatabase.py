from typing import List

import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel

# SQLAlchemy specific code, as with any other app
DATABASE_URL = "sqlite:///weather.sqlite"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

database = databases.Database(DATABASE_URL)