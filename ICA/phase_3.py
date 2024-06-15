# Importing necessary modules from phase 1 and phase 2
import phase_1 
# import phase_2 
import sqlite3

# User input methods
def get_user_action():
    action = int(input("""Select an action:
                    0 = Select all countries
                    1 = Select all cities
                    2 = Get the average temperature for a city in a given year
                    3 = Get a 7-day precipitation for a city from a date
                    4 = Get the average temperature for a city between two dates
                    5 = Get all cities' average temperature between two dates and plot on BarChart
                    6 = Get the average precipitation for all countries for a year and plot on a Bar Chart
                    7 = Show multi-chart for the average Min and Max temps per city
                    Enter here > """))
    return action

# Validation for the selected action
def validate_user_action():
    while True:
        try:
            action = get_user_action()

            if action not in range(8):
                print("Enter a valid number.")
                try:
                    action = get_user_action()
                except ValueError:
                    print("Enter a valid number.")
            else:
                print("You have to chosen an action", action)
                return action
        except ValueError:
            print("Enter a valid number.")

# Asking if the user wants to perform another action
def ask_another_action():
    while True:
        try:
            action = int(input("""Would you like to select another action?
                                1 = Yes
                                2 = No
                                """))
            if action < 1 or action > 2:
                print("Enter either 1 or 2.")
            else:
                return action
        except ValueError:
            print("Input a number.")

# Connecting to the database
with sqlite3.connect("..\\db\\CIS4044-N-SDI-OPENMETEO-PARTIAL.db") as connection:
    while True:
        validated = 0

        if validated == 2:
            break
        action = validate_user_action()

        if action == 0:
            print("Here is a list of all the countries")
            phase_1.select_all_countries(connection)
            validated = ask_another_action()
            if validated == 2:
                print("Goodbye")
                break

        elif action == 1:
            print("Here is a list of all the cities")
            phase_1.select_all_cities(connection)
            validated = ask_another_action()
            if validated == 2:
                print("Goodbye")
                break

        elif action == 2:
            while True:
                try:
                    year = int(input("Enter a year between 2000 and 2022, e.g., 2015: "))
                    city_id = int(input("Enter the ID number for the city between 1-4: "))

                    if year < 2000 or year > 2022:
                        print("Enter a year between 2000 and 2022.")
                    elif city_id < 1 or city_id > 4:
                        print("Enter a city_id between 1 - 4.")
                    else:
                        phase_1.average_annual_temperature(connection, city_id, year)
                        break

                except ValueError:
                    print("Enter a valid integer.")

            validated = ask_another_action()
            if validated == 2:
                print("Goodbye")
                break
