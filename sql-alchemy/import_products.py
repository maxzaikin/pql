import csv
from db import (
    Model,
    Session,
    engine
)
from models import(
    Product,
    Manufacturer
)
from sqlalchemy.exc import SQLAlchemyError

def main(csv_file: str):
    Model.metadata.drop_all(engine) # This deletes all data
    Model.metadata.create_all(engine)
    
    try:
        # Start a database session using the double context manager method, so
        # that all the changes made in the session are automatically committed at the end.
        with Session() as session:
            with session.begin():
                # Third context manager dedicated to opening the CSV file that contains the data to import. Using a context manager 
                # when opening a file is very convenient, as this ensures that the file is automatically closed at the end.            
                with open(csv_file) as f:
                    reader= csv.DictReader(f)
                    all_manufacturers = {}
                    
                    for row in reader:
                        
                        # A Product model instance is created directly by passing the contents of each row
                        # dictionary as keyword arguments. Each of these product model instances is then
                        # added to the database session.
                        # When the for-loop that iterates over the rows of the CSV file exits, the
                        # session.begin() context manager will flush and commit the session, and the
                        # outer context manager will then close the session. The flush operation will write
                        # all the products imported from the CSV file to a database transaction, and the
                        # commit operation will then make these changes permanent.

                        row['year']= int(row['year'])
                        manufacturer = row.pop('manufacturer')
                        p= Product(**row)
                        
                        # The manufacturer name is checked for existence in the all_manufacturers dictionary. When not found, a 
                        # new Manufacturer object is created and initialized with that name. The new manufacturer object is added to the
                        # SQLAlchemy session so that it is later saved.
                        if manufacturer not in all_manufacturers:
                            m= Manufacturer(name=manufacturer)
                            session.add(m)
                            all_manufacturers[manufacturer]=m
                        
                        # the new product is appended to the products relationship of the manufacturer, which works similarly to a list. This products
                        # relationship object, which represents the "many" side, has append() and remove() methods, allowing applications to add or 
                        # remove objects from the relationship using the familiar list syntax. SQLAlchemy automatically translates
                        # these operations to the corresponding foreign key changes.
                        #
                        # the append() call on the products relationship attribute achieves two things: 
                        # 1. it links the manufacturer to the product through the manufacturer_id foreign key, which will be automatically set when the session is 
                        #    committed; 
                        # 2. it indirectly includes the new product in the database session, because it is referenced by the manufacturer
                        #    instance which has been explicitly added before. An explicit session.add(p) for the product would not cause any harm, 
                        #    but it isn't necessary. This automatic addition of a child to the session when the parent is already in it is called a cascade.
                        all_manufacturers[manufacturer].products.append(p)
        
    except FileNotFoundError:
        print(f'{csv_file} not found.')
    except SQLAlchemyError as er:
        print(f'DB error: {er}')
    except Exception as ex:
        print(f'Undefined exception: {ex}')
    
                    
if __name__=='__main__':   
    main(csv_file='products.csv')