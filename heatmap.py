import seaborn as sns
import pandas as pd
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
    SELECT Restaurants.name, 
           MAX(RestaurantCheckinSummary.checkin_count) AS checkin_count, 
           AVG(Inspections.score) AS average_score
    FROM Restaurants
    JOIN Inspections ON Restaurants.restaurant_id = Inspections.restaurant_id
    JOIN RestaurantCheckinSummary ON Inspections.restaurant_id = RestaurantCheckinSummary.restaurant_id
    GROUP BY Restaurants.name
    ORDER BY checkin_count ASC LIMIT 30;
""")

# Execute the query and fetch the results
result = session.execute(query).fetchall()

data = [(row[0], float(row[1]), float(row[2])) for row in result]

# # Extracting columns from the result
restaurant_ids, checkin_counts, average_scores = zip(*data)

data = {
    'Restaurant_ID': restaurant_ids,
    'Checkin_Count': checkin_counts,
    'Average_Score': average_scores
}

# print(data)

df = pd.DataFrame(data)
df.set_index('Restaurant_ID', inplace=True)

# Create heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(df, annot=True, cmap='YlGnBu', fmt='.1f', linewidths=0.5)
plt.title('Heatmap: Check-in Counts and Average Scores')
plt.xlabel('Metrics')
plt.ylabel('Restaurant IDs')

plt.show()
