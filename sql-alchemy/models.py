from sqlalchemy import (
    String,
    ForeignKey,
    Table,
    Column,
    Text
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
    WriteOnlyMapped
)

# The problem with the auto-incrementing integer primary keys used earlier is that
# when they are included in URLs or emails, they indirectly allow people to
# estimate the size of the database tables they reference. Most business will
# probably prefer to keep the number of customers or orders they have private, so
# using integer keys for these tables is not a good idea.
from uuid import (
    UUID,
    uuid4
)
from typing import Optional
from datetime import datetime
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
    
    order_items: WriteOnlyMapped['OrderItem']= relationship(back_populates='product')
    
    reviews: WriteOnlyMapped['ProductReview']= relationship(back_populates='product')
    
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
    
class Order(Model):
    __tablename__= 'orders'
    # The id columns above pass the uuid4 function as default, so that each new item gets its own newly generated UUID4. When
    # passing functions as default column values it is important to remember to not include the () after the function name. SQLAlchemy needs the reference to the
    # function itself, so that it can call it when a value needs to be generated.
    id: Mapped[UUID]= mapped_column(default=uuid4, primary_key=True)
    # when adding an order, the current date and time will be automatically set during the commit operation.
    timestamp: Mapped[datetime]= mapped_column(default=datetime.utcnow, index=True)
    # The one-to-many relationship between customers and orders is established by adding a foreign key on the "many" side
    customer_id: Mapped[UUID]= mapped_column(ForeignKey('customers.id'), index=True)
    
    customer: Mapped['Customer']= relationship(back_populates='orders')
    
    order_items: Mapped[list['OrderItem']]= relationship(back_populates='order')
    
    def __repr__(self):
        return f'Order({self.id.hex})'

class Customer(Model):
    __tablename__='customers'
    
    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    name: Mapped[str]= mapped_column(String(64), index=True, unique=True)
    address: Mapped[Optional[str]]= mapped_column(String(128))
    phone: Mapped[Optional[str]]= mapped_column(String(32))
    # the lazy='write_only' option write_only relationship is that a lazily evaluated one isn't very useful for it. This could potentially be a long
    # relationship for repeat customers, and getting the entire collection of orders from a customer as a list is unlikely to be very useful.
    # it does not attempt to load the relationship, it just generates a query object that you can execute yourself
    orders: WriteOnlyMapped['Order']= relationship(back_populates='customer')
    
    product_reviews: WriteOnlyMapped['ProductReview']= relationship(back_populates='customer')
    
    def __repr__(self):
        return f'Customer({self.id.hex}, "{self.name}")'
    
    
# Association Object Pattern - alternative method to define a many-to-many relationship
# many-to-many relationship needs extra data, the join table is created as a Model subclass, to allow the application to manage the additional columns
class OrderItem(Model):
    __tablename__='order_item'
        
    product_id: Mapped[int]= mapped_column(ForeignKey('products.id'), primary_key=True)
    order_id: Mapped[UUID]= mapped_column(ForeignKey('orders.id'), primary_key=True)
    
    product: Mapped['Product']= relationship(back_populates='order_items')
    order: Mapped['Order']= relationship(back_populates='order_items')
        
    unit_price: Mapped[float]
    quantity: Mapped[int]
    
class ProductReview(Model):
    __tablename__='product_reviews'
    
    product_id: Mapped[int]= mapped_column(ForeignKey('products.id'), primary_key=True)
    customer_id: Mapped[UUID]= mapped_column(ForeignKey('customers.id'), primary_key=True)
    timestamp: Mapped[datetime]= mapped_column(default=datetime.utcnow, index=True)
    rating: Mapped[int]
    comment: Mapped[Optional[str]]= mapped_column(Text)
    
    product: Mapped['Product']= relationship(back_populates='reviews')
    
    customer: Mapped['Customer']= relationship(back_populates='product_reviews')