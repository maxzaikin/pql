import os
from dotenv import load_dotenv
from sqlalchemy import (
    create_engine,
    MetaData
)
from sqlalchemy.orm import (
    DeclarativeBase,
    sessionmaker
)

class Model(DeclarativeBase):
    metadata= MetaData(
        naming_convention={
            'ix': 'ix_%(column_0_label)s',
            'uq': 'uq_%(table_name)s_%(column_0_name)s',
            'ck': 'ck_%(table_name)s_%(constraint_name)s',
            'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
            'pk': 'pk_%(table_name)s'
            
        }
    )

# Load db.env file in memory
load_dotenv(dotenv_path='./db.env')

engine= create_engine(os.getenv('DATABASE_URL'), echo=True) # echo=True - way to spy on the database activity

# Session objects are available only for applications that use the ORM module.
# When using Core, database transactions have to be manually managed by issuing
# appropriate SQL statements through an engine connection.

Session= sessionmaker(engine)

