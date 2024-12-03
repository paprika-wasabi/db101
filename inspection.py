from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

# Define the base class for all models
Base = declarative_base()

# Define the Inspection ORM class (for the Inspections table)
class Inspection(Base):
    __tablename__ = 'Inspections'

    inspection_id = Column(Integer, primary_key=True, autoincrement=True)  # inspection_id
    restaurant_id = Column(Integer, ForeignKey('Restaurants.restaurant_id'))  # Foreign key
    violation_description = Column(Text, nullable=True)
    score = Column(Integer, nullable=True)
    grade = Column(String(1), nullable=True)
    CAMIS = Column(BigInteger, nullable=False)

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
def insert_inspection(restaurant_id, violation_description, score, grade, CAMIS):
    new_inspection = Inspection(
        restaurant_id=restaurant_id,
        violation_description=violation_description,
        score=score,
        grade=grade,
        CAMIS=CAMIS
    )
    session.add(new_inspection)
    session.commit()

# Example: Fetch all inspections for a restaurant
def get_inspections_for_restaurant(restaurant_id):
    inspections = session.query(Inspection).filter(Inspection.restaurant_id == restaurant_id).all()
    for inspection in inspections:
        print(f"Inspection ID: {inspection.inspection_id}, Violation: {inspection.violation_description}, Score: {inspection.score}, Grade: {inspection.grade}")

# Close the session
session.close()
