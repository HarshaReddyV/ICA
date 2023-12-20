# Author: <Harsha Vanga>
# Student ID: <C2285085>

import sqlite3
from tabulate import tabulate
from datetime import datetime,timedelta
from utils import get_connection

connection = get_connection()

def select_all_countries():
    try:  
        query = "SELECT * from [countries]"
        cursor = connection.cursor()
        results = cursor.execute(query).fetchall()
        
        table = []
        head = ["Country ID", "Country Name", "Time Zone"]
        for row in results: 
            data = [row[0], row[1],row[2]]
            table.append(data)
   
        print(tabulate(table, head, tablefmt="grid"))    
        return True   
    except sqlite3.OperationalError as ex:
        print(ex)

def select_all_cities():
    try:  
        query = "SELECT * from [cities]"
        cursor = connection.cursor()
        results = cursor.execute(query).fetchall()

        table = []
        head = ["City ID","City Name", "Longitude", "Latitude", "Country ID"]

        for row in results: 
            data = [row[0], row[1],row[2],row[3],row[4]]
            table.append(data)

        print(tabulate(table, head, tablefmt="grid"))    
        return True   
           
    except sqlite3.OperationalError as ex:
        print(ex)
    

def average_annual_temperature( city_id, year):
    query = f"SELECT AVG(mean_temp) FROM [daily_weather_entries] WHERE city_id = '{city_id}' AND date BETWEEN '{year}-01-01' AND '{year}-12-31'"
    city_query =  f"SELECT [name] from [cities] WHERE id == '{city_id}' "
    cursor = connection.cursor()
    result = cursor.execute(query).fetchone()
    city = cursor.execute(city_query).fetchone()
    city = city[0]
    result = result[0]

    print(f"\nThe Average Annual Temperature in {city} in {year} is {result:.2f}\n")

def average_seven_day_precipitation( city_id, start_date):
    cursor = connection.cursor()
    city_query =  f"SELECT [name] from [cities] WHERE id == '{city_id}' "
    city = cursor.execute(city_query).fetchone()
    city = city[0]

    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = start_date + timedelta(days=7)
    
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    
    query = f"SELECT AVG(precipitation) FROM [daily_weather_entries] WHERE city_id = '{city_id}' AND date BETWEEN '{start_date}' AND '{end_date}' "
    result = cursor.execute(query).fetchone()
    result = result[0]

    if result is None:
        print('Cannot Find the Data for Given Query..Please check the Date Range')
        exit()
    
    print(f"***\nThe Average Seven Day Precipitation in {city} from {start_date} and {end_date} is {result:.2f}\n***")
    pass

def average_mean_temp_by_city( date_from, date_to):
    query = f"SELECT c.name, AVG(d.mean_temp) FROM [daily_weather_entries] d JOIN cities c ON d.city_id = c.id WHERE d.date BETWEEN '{date_from}' AND '{date_to}' GROUP BY d.city_id "
    cursor = connection.cursor()
    result = cursor.execute(query).fetchall()
    if not result:
        print(f'\n Data Not Found: Please Check the Date Range and Enter Valid Date Range\n')
        exit()
    table = []
    head = ["City",f"Average Temperature from {date_from} to {date_to}"]
    for row in result: 
        data = [row[0], f"{row[1]:.2f}"]
        table.append(data)

    print(tabulate(table, head, tablefmt="grid"))    
    return result

def average_annual_precipitation_by_country( year):

    query = f"SELECT c.name, AVG(d.precipitation) FROM [daily_weather_entries] d JOIN [countries] c ON d.city_id = c.id JOIN [cities] j ON j.country_id = c.id WHERE d.date BETWEEN '{year}-01-01' AND '{year}-12-31' GROUP BY c.id "
    cursor = connection.cursor()
    result = cursor.execute(query).fetchall()

    table = []
    head = ["Country",f"Average Annual Precepitation in {year}"]

    for row in result: 
        data = [row[0], f"{row[1]:.2f}"]
        table.append(data)

    print(tabulate(table, head, tablefmt="grid"))    
    pass


if __name__ == "__main__":
    select_all_countries()
    select_all_cities()
    average_annual_temperature( '1', '2022')
    average_seven_day_precipitation( '1', '2021-12-02')
    average_mean_temp_by_city( '2022-12-02', '2022-12-09')
    average_annual_precipitation_by_country( '2022')
    pass
