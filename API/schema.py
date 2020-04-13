"""
Setup Notes:
https://docs.sqlalchemy.org/en/13/orm/tutorial.html

On relationship with Base/Inheritance
https://docs.sqlalchemy.org/en/13/orm/inheritance.html#joined-table-inheritance
"""


"""
The idea for this py file is to structure the schema. We can create a transform
file that wrangles the data and is then pushed to another file that writes
in the data into the database.
"""

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
