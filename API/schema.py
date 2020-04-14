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

Previous Cohorts Schema can be found at: https://www.notion.so/DB_deets-8b127e040ef8452583b62e79b883e3e6

When getting data, we need to decide how our tables will be structured and
modify the code in this file accordingly.
"""


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integr, String, ForeignKey, DateTime, Float, Text, Boolean, UniqueConstraint, ForeignKeyConstraint
Base = declarative_base()


# Table Schemas

class Visions():
    """
    Google Vision API Table
    """
    vision_id = Column(Integer, primary_key=True)

    def to_json():
        """
        Endpoint should return as a json object for frontend.
        """
        pass


class Ingredients():
    """
    Ingredient Table(Draft, needs to be adjusted as we get more data.)
    """
    ingredient_id = Column(Integer)
    name = Column(String, primary_key=True)
    category = Column(String)


class Recipes():
    """
    Recipes Table
    """
    recipe_id = Column(Integer, primary_key=True)


class Instructions():
    """
    Instructions Table.

    Instructions does not have to be its own table, it can be an 'element'
    of ingredients. 
    """
    instruction_id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer)
