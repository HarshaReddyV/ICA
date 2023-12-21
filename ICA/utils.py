import sqlite3
from geopy.geocoders import Nominatim

def get_coordinates(city_name):
    geolocator = Nominatim(user_agent="your_app_name")
    location = geolocator.geocode(city_name)
    if location:
        latitude, longitude = location.latitude, location.longitude
        return latitude, longitude
    else:
        return None

def get_connection():
    connection = sqlite3.connect('../db/weather.db')
    return connection

def get_city():
    print('Select from Available Cities')
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT DISTINCT id,name FROM cities ORDER BY id ASC"
    results = cursor.execute(query).fetchall()
    print('*** AVAILABLE CITIES***')
    for result in results: 
        print(f'{result[0]}. {result[1]}')
        
    while True:
        city_id = input('Select City Number:')
        if city_id.isdigit():
            city_id = int(city_id)
            for result in results:
                if city_id == int(result[0]): 
                    city_name = result[1]
                    print(city_name)
                    return (str(city_id),city_name)
        print('Enter a Valid City Nunber\n')
    

def get_year():
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT DISTINCT strftime('%Y', date) FROM daily_weather_entries;"
        cursor.execute(query)
        years = [result[0] for result in cursor.fetchall()]
        cursor.close()
        conn.close()
        print(" ***Years Available in the database:", years)    
        while True:
            year = input('Enter Year(YYYY):')
            if year.isdigit():
                if year in years:
                    return year
            
            print(f'Enter a valid Year\n')

def get_date():
    year = get_year()  
    while True:
        month = input('Enter Month Number(MM):').strip()
        if month.isdigit():
            if int(month) >= 1 and int(month)<= 12:
                break
        print(f'Enter a Valid Month Number..!\n')
    
    while True:
        day = input('Enter Day Number(DD):').strip()
        if month.isdigit():
            if int(month) >= 1 and int(month)<= 31:
                break
            print(f'Enter a Valid Day Number..!\n')

    date = f'{year}-{month}-{day}'
    return date


def get_month():
    i = 1    
    months = ['January','February','March','April','May','June','July','August','September','October','November','Decemeber']
    for month in months:
        print(f'{i}.{month}')
        i += 1

    while True:
        selected_month = input('Enter month Number:')
    
        if selected_month.isdigit() and  1 <= int(selected_month) <=12:
            return selected_month, months[int(selected_month) - 1]
        print('Enter a Valid Month Number..!')


