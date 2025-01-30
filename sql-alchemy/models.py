from sqlalchemy import (
    String,
    ForeignKey,
    Table,
    Column
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from typing import Optional

from db import Model

# Join table in order to build many-many relationship
ProductCountry= Table(
    'products_countries',
    Model.metadata,
    Column('prpduct_id', ForeignKey('products.id'), primary_key=True, nullable= False),
    Column('country_id', ForeignKey('countries.id'), primary_key=True, nullable=False)
)    

# all application model classes must inherit from the Model declarative base class
#
# The Mapped[t] type declaration is used to define each column, with t being the
# Python type assigned to the column, such as int, str, or datetime.
class Product(Model):
    __tablename__ = 'products'
    
    id: Mapped[int]= mapped_column(primary_key=True)
    name: Mapped[str]= mapped_column(String(64), index=True,unique=True)
    # The new manufacturer_id column is a FK integer, matching the type of the primary key of the new Manufacturer model.
    manufacturer_id: Mapped[int]= mapped_column(ForeignKey('manufacturers.id'), index=True)
    year: Mapped[int] = mapped_column(index=True)
    cpu: Mapped[Optional[str]]= mapped_column(String(32))
    
    # Thr manufacturer attribute represents the relationship as seen from the "many" side in one-to-many relationship. This attribute is not a column 
    # that is physically stored in the database; it is a high-level replacement of manufacturer_id that transparently loads the related model object.
    manufacturer: Mapped['Manufacturer']= relationship(back_populates='products', lazy='joined') # joined eagerly loading all related data avaoiding lazy load
    
    # Add many-many relationship. The secondary argument to relationship() tells SQLAlchemy that this
    # relationship is supported by a secondary table (the join table)
    countries: Mapped[list['Country']]= relationship(secondary=ProductCountry, back_populates='products')
    
    def __repr__(self):
        return f'Product({self.id}, "{self.name}")'
    
class Country(Model):
    __tablename__='countries'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]= mapped_column(String(32), index=True, unique=True)
    
    products: Mapped[list['Product']]= relationship(secondary=ProductCountry, back_populates='countries')
    
class Manufacturer(Model):
    __tablename__= 'manufacturers'
    
    id: Mapped[int]=  mapped_column(primary_key=True)
    name: Mapped[str]= mapped_column(String(64), index=True, unique=True)
    
    products: Mapped[list['Product']]= relationship(cascade='all, delete-orphan', back_populates='manufacturer')
    
    def __repr__(self):
        return f'Manufacturer({self.id}, "{self.name}")'
    

