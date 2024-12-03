import folium
from folium.plugins import HeatMap
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

# Assuming these models are already defined:
# Restaurant, Inspections, RestaurantCheckinSummary

# Create an engine to connect to the database
DATABASE_URL = "mysql+mysqlconnector://root:my-secret-pw@localhost/restaurants_analysis"
engine = create_engine(DATABASE_URL)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Lowest average score for restaurants with more than 30 average score.
# query = text("""
#     SELECT ST_AsText(Restaurants.location)
#     FROM Restaurants
#     JOIN Inspections ON Restaurants.restaurant_id = Inspections.restaurant_id
#     JOIN RestaurantCheckinSummary ON Inspections.restaurant_id = RestaurantCheckinSummary.restaurant_id
#     GROUP BY Restaurants.location
#     HAVING AVG(score) > 30
#     ORDER BY AVG(score) DESC LIMIT 1000;
# """)

query = text("""SELECT ST_AsText(Restaurants.location)
FROM Restaurants
WHERE Restaurants.cuisine_type = 'Indian'""" )

# Execute the query
result = session.execute(query).fetchall()

# Convert POINT strings to tuples
coordinates = []
for record in result:
    point_str = record[0]  # Extract the string from the tuple
    lat_lon = point_str.strip('POINT()').split()  # Remove 'POINT()' and split into lat and lon
    lat, lon = float(lat_lon[0]), float(lat_lon[1])  # Convert to floats
    coordinates.append([lat, lon])

# Create a map centered around NYC
nyc_map = folium.Map(location=[40.712776, -74.005974], zoom_start=12)

# Add the heatmap layer
HeatMap(coordinates).add_to(nyc_map)

# Save map to HTML
nyc_map.save('nyc_heatmap.html')
