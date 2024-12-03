import pandas as pd
import mysql.connector
import restaurant
import inspection
from mysql.connector import Error

# Set up MySQL connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',        # Change to your MySQL host
            database='restaurants_analysis',  # Change to your database name
            user='root',      # Change to your MySQL username
            password='my-secret-pw'   # Change to your MySQL password
        )
        if connection.is_connected():
            print("Connected to MySQL")
        return connection
    except Error as e:
        print("Error while connecting to MySQL", e)

# Read CSV file using pandas
def read_csv(file_path):
    df = pd.read_csv(file_path, usecols=
                     ['CAMIS',
                      'DBA',
                      'CUISINE DESCRIPTION', 
                      'Latitude', 
                      'Longitude',
                      'VIOLATION DESCRIPTION',
                      'SCORE',
                      'GRADE'])
    return df

def is_valid_data(row):
    if not row.get('CAMIS') or not row.get('DBA') or not row.get('CUISINE DESCRIPTION') or \
       not row.get('Latitude') or not row.get('Longitude') or \
       not row.get('VIOLATION DESCRIPTION') or not row.get('SCORE') or \
       not row.get('GRADE'):
        return False  # Invalid row if any field is missing or empty
    if (row['CAMIS'] == '' or row['DBA'] == '' 
        or row['CUISINE DESCRIPTION'] == ''
        or row['Latitude'] == '' 
        or row['Longitude'] == '' 
        or row['VIOLATION DESCRIPTION'] == '' 
        or row['SCORE'] == '' 
        or row['GRADE'] == ''):
        return False

# Insert Data into MySQL table
def insert_into_mysql(df):
    for i, row in df.iterrows():
        try:
            if is_valid_data(row) == False:
                continue
            restaurantId = restaurant.insert_restaurant(
                row['DBA'], 
                row['Latitude'], 
                row['Longitude'], 
                row['CUISINE DESCRIPTION'],
                row['CAMIS'])
            inspection.insert_inspection(
                restaurantId, 
                row['VIOLATION DESCRIPTION'], 
                row['SCORE'], 
                row['GRADE'],
                row['CAMIS'])   
        except Exception as e:
            continue
    

# # Main execution
create_connection()
file_path = 'eidp\DB101\db101.cleaned_inspections.csv'  # Replace with the path to your CSV file
df = read_csv(file_path)
insert_into_mysql(df)
