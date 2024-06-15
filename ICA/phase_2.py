import sqlite3
import matplotlib.pyplot as plt
from datetime import timedelta, datetime


def plot_average_temperature_cities(connection, start_date, end_date):
    try:
        connection.row_factory = sqlite3.Row
        # Define the query to get average temperatures for each city within the specified date range
        query = """
        SELECT AVG(mean_temp) as avg_temperature, cities.name as city_name 
        FROM daily_weather_entries
        JOIN cities ON daily_weather_entries.city_id = cities.id
        WHERE date BETWEEN ? AND ?
        GROUP BY cities.name
        """
        
        # Get a cursor object from the database connection
        cursor = connection.cursor()

        # Execute the query via the cursor object, using placeholders
        results = cursor.execute(query, (start_date, end_date))

        # Fetch all rows from the results
        rows = results.fetchall()

        if rows:
            # Extract city names and average temperatures from the results
            city_names = [row['city_name'] for row in rows]
            avg_temperatures = [row['avg_temperature'] for row in rows]

            # Plotting the bar chart
            plt.bar(city_names, avg_temperatures, color='skyblue')
            plt.title(f"Average Temperature of Cities from {start_date} to {end_date}")
            plt.xlabel("Cities")
            plt.ylabel("Average Temperature")
            plt.xticks(rotation=45, ha='right')
            
            # Add data labels to each bar
            for city, avg_temp in zip(city_names, avg_temperatures):
                plt.text(city, avg_temp, f'{avg_temp:.2f}', ha='center', va='bottom')

            plt.tight_layout()

            # Display the bar chart
            plt.show()
        else:
            print(f"No data found for the specified time period.")

    except sqlite3.OperationalError as ex:
        print(ex)

def plot_annual_precipitation_by_country(connection, year):
    try:
        connection.row_factory = sqlite3.Row
        # Define the start and end dates for the specified year
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"

        # Define the query with placeholders for start_date and end_date
        query = """
        SELECT round(AVG(precipitation), 2) as avg_precipitation, countries.name as country_name 
        FROM daily_weather_entries 
        JOIN cities ON daily_weather_entries.city_id = cities.id
        JOIN countries ON cities.country_id = countries.id
        WHERE date BETWEEN ? and ?
        GROUP BY countries.name
        """

        # Get a cursor object from the database connection
        cursor = connection.cursor()

        # Execute the query via the cursor object, using placeholders
        results = cursor.execute(query, (start_date, end_date))

        # Fetch all rows from the results
        rows = results.fetchall()

        if rows:
            # Extract country names and average precipitations from the results
            country_names = [row['country_name'] for row in rows]
            avg_precipitations = [row['avg_precipitation'] for row in rows]

            # Plotting the bar chart
            plt.bar(country_names, avg_precipitations, color='lightblue')
            plt.title(f"Annual Precipitation for Countries in {year}")
            plt.xlabel("Countries")
            plt.ylabel("Average Precipitation")
            plt.xticks(rotation=45, ha='right')

            # Add data labels to each bar
            for country, avg_precipitation in zip(country_names, avg_precipitations):
                plt.text(country, avg_precipitation, f'{avg_precipitation:.2f}', ha='center', va='bottom')

            plt.tight_layout()

            # Display the bar chart
            plt.show()
        else:
            print(f"No data found for the specified time period.")

    except sqlite3.OperationalError as ex:
        print(ex)
   
def plot_seven_day_precipitation(connection, city_id, start_date):
    try:
        connection.row_factory = sqlite3.Row

        # Calculate the end date by adding 6 days to the start date
        end_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=6)).strftime("%Y-%m-%d")

        # Define the query
        query = f"""
        SELECT date, precipitation
        FROM daily_weather_entries
        WHERE date BETWEEN ? AND ? AND city_id = ?
        """

        # Get a cursor object from the database connection
        cursor = connection.cursor()

        # Execute the query via the cursor object, using placeholders
        results = cursor.execute(query, (start_date, end_date, city_id))

        # Fetch all rows from the results
        rows = results.fetchall()

        if rows:
            # Extract dates and precipitation values from the results
            dates = [row['date'] for row in rows]
            precipitation_values = [row['precipitation'] for row in rows]

            # Plotting the bar chart
            plt.bar(dates, precipitation_values, color='lightgreen')
            plt.title(f"7-Day Precipitation for City {city_id}")
            plt.xlabel("Date")
            plt.ylabel("Precipitation")
            plt.xticks(rotation=45, ha='right')

            # Add data labels to each bar
            for date, precipitation in zip(dates, precipitation_values):
                plt.text(date, precipitation, f'{precipitation:.2f}', ha='center', va='bottom')

            plt.tight_layout()

            # Display the bar chart
            plt.show()
        else:
            print(f"No data found for the specified time period.")

    except sqlite3.OperationalError as ex:
        print(ex)


def plot_grouped_bar_chart(connection, start_date, end_date):
    try:
        connection.row_factory = sqlite3.Row

        # Query to retrieve city information
        city_query = "SELECT id, name FROM cities"
        cursor = connection.cursor()
        cities = cursor.execute(city_query).fetchall()

        if not cities:
            print("No cities found in the database.")
            return

        # Display available cities to the user
        print("Available Cities:")
        for city in cities:
            print(f"{city['id']}. {city['name']}")

        # Prompt user for city selection
        selected_city_id = input("Enter the ID of the city you want to plot data for: ")

        # Validate user input
        selected_city = next((city for city in cities if str(city['id']) == selected_city_id), None)
        if not selected_city:
            print("Invalid city ID. Please enter a valid city ID.")
            return

        # Define the query to retrieve temperature and precipitation data
        query = """
        SELECT MIN(mean_temp) as min_temp, MAX(mean_temp) as max_temp, AVG(mean_temp) as avg_temp,
               AVG(precipitation) as avg_precipitation
        FROM daily_weather_entries
        WHERE date BETWEEN ? AND ? AND city_id = ?
        """

        # Execute the query via the cursor object, using placeholders
        results = cursor.execute(query, (start_date, end_date, selected_city['id']))

        # Fetch a row from the results
        row = results.fetchone()

        if row:
            # Extract data for plotting
            min_temp = row['min_temp']
            max_temp = row['max_temp']
            avg_temp = row['avg_temp']
            avg_precipitation = row['avg_precipitation']

            # Plotting the grouped bar chart
            bar_width = 0.35
            index = range(4)

            bars = plt.bar(index, [min_temp, max_temp, avg_temp, avg_precipitation], width=bar_width, color=['skyblue', 'lightgreen', 'lightcoral', 'lightgray'])

            # Add data labels on top of each bar
            for bar, value in zip(bars, [min_temp, max_temp, avg_temp, avg_precipitation]):
                plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{value:.2f}', ha='center', va='bottom')

            plt.xlabel('Metrics')
            plt.ylabel('Values')
            plt.title(f'Temperature and Precipitation Data for {selected_city["name"]} ({start_date} to {end_date})')
            plt.xticks([i for i in index], ['Min Temperature', 'Max Temperature', 'Avg Temperature', 'Avg Precipitation'])
            
            plt.tight_layout()

            # Display the grouped bar chart
            plt.show()
        else:
            print(f"No data found for the specified time period or city.")

    except sqlite3.OperationalError as ex:
        print(ex)

def plot_daily_temperature(connection, city_id, year, month):
    try:
        connection.row_factory = sqlite3.Row

        # Define the start and end dates for the specified month
        start_date = f"{year}-{month:02d}-01"
        end_date = f"{year}-{month:02d}-{31 if month in [1, 3, 5, 7, 8, 10, 12] else 30 if month != 2 else 28}"

        # Query to retrieve daily minimum and maximum temperatures
        query = """
        SELECT date, MIN(mean_temp) as min_temp, MAX(mean_temp) as max_temp
        FROM daily_weather_entries
        WHERE date BETWEEN ? AND ? AND city_id = ?
        GROUP BY date
        ORDER BY date
        """

        # Execute the query via the cursor object, using placeholders
        cursor = connection.cursor()
        results = cursor.execute(query, (start_date, end_date, city_id))

        # Fetch all rows from the results
        rows = results.fetchall()

        if rows:
            # Convert date strings to datetime objects
            dates = [datetime.strptime(row['date'], "%Y-%m-%d") for row in rows]
            min_temps = [row['min_temp'] if row['min_temp'] is not None else 0 for row in rows]
            max_temps = [row['max_temp'] if row['max_temp'] is not None else 0 for row in rows]

            # Plotting the multi-line chart
            plt.figure(figsize=(10, 6))
            plt.plot(dates, min_temps, label='Min Temperature', marker='o', linestyle='-', color='skyblue')
            plt.plot(dates, max_temps, label='Max Temperature', marker='o', linestyle='-', color='lightcoral')

            # # Adding data labels
            # for date, min_temp, max_temp in zip(dates, min_temps, max_temps):
            #     plt.text(date, min_temp, f'{min_temp:.2f}', ha='left', va='bottom', color='black')
            #     plt.text(date, max_temp, f'{max_temp:.2f}', ha='left', va='top', color='black')

            plt.xlabel('Date')
            plt.ylabel('Temperature (°C)')
            plt.title(f'Daily Minimum and Maximum Temperatures for City {city_id} in {year}-{month:02d}')
            plt.xticks(rotation=45)
            plt.legend()
            plt.tight_layout()

            # Display the multi-line chart
            plt.show()
        else:
            print(f"No data found for the specified time period or city.")

    except sqlite3.OperationalError as ex:
        print(ex)

def scatter_temperature_vs_rainfall(connection, location_type, location_id, start_date, end_date):
    try:
        connection.row_factory = sqlite3.Row

        # Define the query to retrieve temperature and rainfall data
        if location_type == 'city':
            query = """
            SELECT mean_temp, precipitation
            FROM daily_weather_entries
            WHERE date BETWEEN ? AND ? AND city_id = ?
            """
            params = (start_date, end_date, location_id)
        elif location_type == 'country':
            query = """
            SELECT AVG(mean_temp) as mean_temp, AVG(precipitation) as precipitation
            FROM daily_weather_entries
            JOIN cities ON daily_weather_entries.city_id = cities.id
            WHERE date BETWEEN ? AND ? AND cities.country_id = ?
            """
            params = (start_date, end_date, location_id)
        elif location_type == 'all_countries':
            query = """
            SELECT AVG(mean_temp) as mean_temp, AVG(precipitation) as precipitation
            FROM daily_weather_entries
            """
            params = ()
        else:
            print("Invalid location type.")
            return

        # Execute the query via the cursor object, using placeholders
        cursor = connection.cursor()
        results = cursor.execute(query, params)

        # Fetch all rows from the results
        rows = results.fetchall()

        if rows:
            # Extracting temperature and rainfall data
            temperatures = [row['mean_temp'] for row in rows]
            rainfall = [row['precipitation'] for row in rows]

            # Plotting the scatter plot
            plt.figure(figsize=(10, 6))
            plt.scatter(temperatures, rainfall, c='blue', alpha=0.7)
            
            plt.xlabel('Mean Temperature (°C)')
            plt.ylabel('Precipitation (mm)')
            plt.title(f'Scatter Plot: Temperature vs Rainfall ({location_type.capitalize()})')
            plt.grid(True)
            plt.tight_layout()

            # Display the scatter plot
            plt.show()
        else:
            print(f"No data found for the specified time period or location.")

    except sqlite3.OperationalError as ex:
        print(ex)

# Example usage:
        
if __name__ == "__main__":
    with sqlite3.connect("../db/CIS4044-N-SDI-OPENMETEO-PARTIAL.db") as connection:
        plot_average_temperature_cities(connection, "2021-01-01", "2021-12-31")
        plot_annual_precipitation_by_country(connection, "2021")
        plot_seven_day_precipitation(connection, "2", "2021-01-01")
        plot_grouped_bar_chart(connection, '2021-01-01', '2021-12-31')
        plot_daily_temperature(connection, city_id=1, year=2021, month=5)
        # Scatter plot for a specific city
        scatter_temperature_vs_rainfall(connection, location_type='city', location_id=1, start_date='2021-01-01', end_date='2021-12-31')
        # # Scatter plot for a specific country
        # scatter_temperature_vs_rainfall(connection, location_type='country', location_id=1, start_date='2021-01-01', end_date='2021-12-31')
        # # Scatter plot for all countries
        # scatter_temperature_vs_rainfall(connection, location_type='all_countries', location_id=None, start_date='2021-01-01', end_date='2021-12-31')




