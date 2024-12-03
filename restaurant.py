from sqlalchemy import create_engine, Column, Integer, VARCHAR, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import UserDefinedType
from sqlalchemy.sql import text

# Define a custom type for the POINT data type
class Point(UserDefinedType):
    def get_col_spec(self):
        return "POINT"

# Define the base class for all models
Base = declarative_base()

# Define the Restaurant ORM class
class Restaurant(Base):
    __tablename__ = 'Restaurants'  # This will correspond to the 'Restaurants' table in your MySQL database

    # Define the columns based on your table schema
    restaurant_id = Column(Integer, primary_key=True, autoincrement=True)  # Primary Key
    name = Column(VARCHAR(255), nullable=True)
    location = Column(Point, nullable=True)  # This assumes you are storing latitude and longitude as a POINT
    cuisine_type = Column(VARCHAR(50), nullable=True)
    CAMIS = Column(BigInteger, nullable=False)

# MySQL connection string (replace with your credentials)
DATABASE_URL = "mysql+mysqlconnector://root:my-secret-pw@localhost/restaurants_analysis"

# Create an engine to interact with the MySQL database
engine = create_engine(DATABASE_URL)

# Create all tables if they don't already exist
# Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Example: Insert a new restaurant into the Restaurants table
def insert_restaurant(name, latitude, longitude, cuisine_type, CAMIS):
    # First, check if the restaurant already exists based on CAMIS
    check_query = text("SELECT restaurant_id FROM Restaurants WHERE CAMIS = :CAMIS")
    result = session.execute(check_query, {"CAMIS": CAMIS}).fetchone()

    if result:
        # If restaurant exists, return the existing restaurant_id
        return result[0]  # restaurant_id is the first element in the result tuple
    
    location = f"POINT({latitude} {longitude})"
    insert_query = text("""
        INSERT INTO Restaurants (name, location, cuisine_type, CAMIS)
        VALUES (:name, ST_GeomFromText(:location), :cuisine_type, :CAMIS)
    """)
    session.execute(insert_query, {"name": name, "location": location, "cuisine_type": cuisine_type, "CAMIS": CAMIS})
    session.commit()

    # Get the last inserted ID using LAST_INSERT_ID()
    last_insert_id_query = text("SELECT LAST_INSERT_ID()")
    result = session.execute(last_insert_id_query)
    
    # Fetch the last inserted ID
    last_insert_id = result.scalar()
    
    return last_insert_id

# Example: Query all restaurants
def get_all_restaurants():
    restaurants = session.query(Restaurant).all()
    for restaurant in restaurants:
        print(f"Restaurant ID: {restaurant.restaurant_id}, Name: {restaurant.name}, Cuisine: {restaurant.cuisine_type}, Location: {restaurant.location}")

# Close the session
session.close()
