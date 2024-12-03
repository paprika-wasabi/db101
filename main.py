import matplotlib.pyplot as plt
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

# Database connection setup
DATABASE_URL = "mysql+mysqlconnector://root:my-secret-pw@localhost/restaurants_analysis"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Define the SQL query
query = text("""
    SELECT Restaurants.restaurant_id, 
           MAX(RestaurantCheckinSummary.checkin_count) AS checkin_count, 
           AVG(Inspections.score) AS average_score
    FROM Restaurants
    JOIN Inspections ON Restaurants.restaurant_id = Inspections.restaurant_id
    JOIN RestaurantCheckinSummary ON Inspections.restaurant_id = RestaurantCheckinSummary.restaurant_id
    GROUP BY Restaurants.restaurant_id 
    ORDER BY checkin_count DESC;
""")

# Execute the query and fetch the results
result = session.execute(query).fetchall()

data = [(row[0], row[1], round(row[2], 4)) for row in result]

# Extract data
restaurant_ids, checkin_counts, avg_scores = zip(*data)

# Create scatter plot
plt.figure(figsize=(10, 6))
scatter = plt.scatter(avg_scores, checkin_counts, c=avg_scores, cmap='viridis', s=100, edgecolors='k')
plt.colorbar(scatter, label='Average Score')
plt.xlabel('Average Score')
plt.ylabel('Check-in Count')
plt.title('Scatter Plot: Check-in Count vs. Average Score')
plt.grid(True)

plt.show()
