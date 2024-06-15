# Author: <Madonna Tsegha>
# Student ID: <B1215326>

import sqlite3
from multiprocessing import connection
from datetime import datetime, timedelta

# Phase 1 - Starter
# Defning Functions
# Note: Display all real/float numbers to 2 decimal places.

def select_all_countries(connection):
    # Queries the database and selects all the countries 
    # stored in the countries table of the database.
    # The returned results are then printed to the 
    # console.
    try:
        connection.row_factory = sqlite3.Row
        # Define the query
        # Query to select all countries from the database
        query = "SELECT * from [countries]"

        # Get a cursor object from the database connection
        # that will be used to execute database query.
        cursor = connection.cursor()

        # Execute the query via the cursor object.
        results = cursor.execute(query)

        # Iterate over the results and display the results.
        for row in results:
            print(f"Country Id: {row['id']} -- Country Name: {row['name']} -- Country Timezone: {row['timezone']}")

    except sqlite3.OperationalError as ex:
        print(ex)

def select_all_cities(connection):
   # Queries the database and selects all the countries 
   # stored in the countries table of the database.
   # The returned results are then printed to the 
   # console.
    try:
       connection.row_factory = sqlite3.Row
       # Define the query
       query = "SELECT * from [cities]"

       # Get a cursor object from the database connection
       # that will be used to execute database query.
       cursor = connection.cursor()

       # Execute the query via the cursor object.
       results = cursor.execute(query)

       # Iterate over the results and display the results.
       for row in results:
          print(f"City Id: {row['id']} -- City Name: {row['name']} --  Longitude: {row['longitude']}--  Latitude: {row['latitude']} Country ID: {row['country_id']}")
     
    except sqlite3.OperationalError as ex:
        print(ex)

def average_annual_temperature(connection, city_id, year):
   # TODO: Implement this function
   # Find AVG(mean_temp) in daily_weather_entries
    try:
       connection.row_factory = sqlite3.Row
       # Define the query
       query = f"""

       SELECT AVG(mean_temp), name
       FROM daily_weather_entries
       INNER JOIN cities ON daily_weather_entries.city_id = cities.id
       WHERE (date >= '{year}-01-01' AND date <= '{year}-12-31') AND city_id = {city_id}

       """
       print(query)

       # Get a cursor object from the database connection
       # that will be used to execute database query.
       cursor = connection.cursor()

       # Execute the query via the cursor object.
       results = cursor.execute(query)

       # Iterate over the results and display the results.
       for row in results:
        print(f"Average annual temperature for city {city_id} -- {row['name']} in year {year} was {row[0]:.2f}")

    except sqlite3.OperationalError as ex:
        print(ex)

def average_seven_day_precipitation(connection, city_id, start_date):
    # TODO: Implement this function
    # Find AVG(precipitation) in daily_weather_entries
    try:
       connection.row_factory = sqlite3.Row
       # Define the dates       
       # Calculate the end date by adding 6 days to the start date
       end_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days = 6)).strftime("%Y-%m-%d")

       # Define the query
       query = f"""

       SELECT AVG(precipitation) as avg_precipitation, name 
       FROM daily_weather_entries 
       JOIN cities ON daily_weather_entries.city_id = cities.id
       WHERE date BETWEEN {start_date} AND {end_date} AND daily_weather_entries.city_id = {city_id}
       GROUP BY cities.name

       """
       print(f"Query: start_date = {start_date}, end_date = {end_date}, city_id = {city_id}")

       # Get a cursor object from the database connection
       # that will be used to execute database query.
       cursor = connection.cursor()

       # Execute the query via the cursor object.
       results = cursor.execute(query)

       # Fetch a row from the results
       row = results.fetchone()
       if row and row['avg_precipitation'] is not None:
           # Check if value is not none
           print(f"Average seven day precipitation starting from {start_date} to {end_date} in {row['city_name']} is {row['avg_precipitation']:.2f}")
       else:
            print(f"No data found for the time period.")

    except sqlite3.OperationalError as ex:
        print(ex)


def average_mean_temp_by_city(connection, date_from, date_to):
    # TODO: Implement this function
    # Find AVG(mean_temp) in daily_weather_entries by cities_name in cities
    try:
       connection.row_factory = sqlite3.Row
       # Define the query
       query = """
        SELECT 
        AVG(mean_temp) as avg_temperature, cities.name as city_name 
        FROM daily_weather_entries
        JOIN cities ON daily_weather_entries.city_id = cities.id
        WHERE date BETWEEN ? AND ? 
        GROUP BY cities.name
       """
       # Get a cursor object from the database connection
       # that will be used to execute database query.
       cursor = connection.cursor()

       # Execute the query via the cursor object.
       results = cursor.execute(query, (date_from, date_to))

       # Fetch a row from the results
       for row in results:

        if row and row['avg_temperature'] is not None:
            # Check if value is not none
            print(f"Average mean temperature from {date_from} to {date_to} in {row['city_name']} is {row['avg_temperature']:.2f}")
        else:
                print(f"No data found for the time period.")

    except sqlite3.OperationalError as ex:
        print(ex)

def average_annual_precipitation_by_country(connection, year):
    # TODO: Implement this function
    try:
        connection.row_factory = sqlite3.Row
        # Define the start and end dates for the specified year
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"

        # Define the query with placeholders for start_date and end_date
        query = """
        SELECT round(AVG(precipitation),2) as avg_precipitation, countries.name as country_name 
        FROM daily_weather_entries 
        JOIN cities ON daily_weather_entries.city_id = cities.id
        JOIN countries ON cities.country_id = countries.id
        WHERE date BETWEEN ? and ?
        GROUP BY countries.name
        """

        # Get a cursor object from the database connection
        # that will be used to execute database query.
        cursor = connection.cursor()


        # Execute the query via the cursor object, using placeholders
        results = cursor.execute(query, (start_date, end_date))

        # Fetch a row from the results
        rows = results.fetchall()
        if rows:
            # Iterate over the results and display the average precipitation for each country
            for row in rows:
                avg_precipitation = row['avg_precipitation']
                if avg_precipitation is not None:
                    print(f"Average annual precipitation for {row['country_name']} in {year}: {avg_precipitation}")
                else:
                    print(f"No data found for {row['country_name']} in {year}.")
        else:
            print(f"No data found for the specified time period.")

    except sqlite3.OperationalError as ex:
        print(ex)

if __name__ == "__main__":
    # Create a SQLite3 connection and call the various functions
    # above, printing the results to the terminal.
    with sqlite3.connect("..\\db\\CIS4044-N-SDI-OPENMETEO-PARTIAL.db") as connection:
        select_all_countries(connection)
        select_all_cities(connection)
        average_annual_temperature(connection, "1", "2021")
        average_seven_day_precipitation(connection, "2", "2001-01-01")
        average_mean_temp_by_city(connection, "2001-01-01", "2022-01-01")
        average_annual_precipitation_by_country(connection, "2021")
        

# '''
# Additional Codes

# '''

