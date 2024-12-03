import pandas as pd
import restaurant
from sqlalchemy import func
from sqlalchemy import create_engine, Column, Integer, ForeignKey, DateTime, VARCHAR, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import UserDefinedType
from sqlalchemy.orm import sessionmaker
from datetime import datetime

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

# Define the Checkin ORM class (for the CheckIns table)
class Checkin(Base):
    __tablename__ = 'CheckIns'

    checkin_id = Column(Integer, primary_key=True, autoincrement=True)  # inspection_id
    restaurant_id = Column(Integer, ForeignKey('Restaurants.restaurant_id'))  # Foreign key
    user_id = Column(Integer, nullable=False)
    checkin_time = Column(DateTime, nullable=True)

# MySQL connection string (replace with your credentials)
DATABASE_URL = "mysql+mysqlconnector://root:my-secret-pw@localhost/restaurants_analysis"

# Create an engine to interact with the MySQL database
engine = create_engine(DATABASE_URL)

# Create all tables if they don't already exist
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Example: Insert an inspection record
def insert_checkin(restaurant_id, user_id, checkin_time):
    new_checkin = Checkin(
        restaurant_id=restaurant_id,
        user_id=user_id,
        checkin_time=checkin_time
    )
    session.add(new_checkin)
    session.commit()

# Read CSV file using pandas
def read_csv(file_path):
    df = pd.read_csv(file_path, usecols=
                     ['userId',
                      'latitude',
                      'longitude',
                      'utcTimestamp'])
    return df

# Function to find the nearest restaurant
def find_nearest_restaurant(session, latitude: float, longitude: float, max_distance: float):
    point = f"POINT({latitude} {longitude})"  # Ensure correct order: longitude first
    
    # Query to compute distances and filter
    nearest_restaurant = (
        session.query(
            restaurant.Restaurant.restaurant_id,
            restaurant.Restaurant.name,
            func.ST_Distance(restaurant.Restaurant.location, func.ST_GeomFromText(point)).label('distance')
        )
        .filter(func.ST_Distance(restaurant.Restaurant.location, func.ST_GeomFromText(point)) < max_distance)
        .order_by(func.ST_Distance(restaurant.Restaurant.location, func.ST_GeomFromText(point)))
        .limit(1)
        .first()
    )
    
    return nearest_restaurant

def insert_into_mysql(df):
    for i, row in df.iterrows():
        try:
            nearest = find_nearest_restaurant(session, row['latitude'], row['longitude'], 5)  # Distance in meters
            dt_obj = datetime.strptime(row['utcTimestamp'], "%a %b %d %H:%M:%S %z %Y")
            normalized_time = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
            insert_checkin(f"{nearest.restaurant_id}", row['userId'], normalized_time)
        except Exception as e:
            print(e)
            continue

file_path = 'eidp\DB101\db101.cleaned_checkins.csv'
df = read_csv(file_path)
insert_into_mysql(df)