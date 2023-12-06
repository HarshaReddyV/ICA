import sqlite3

def get_connection():
    connection = sqlite3.connect('../db/weather.db')
    return connection

def get_city():
    print(""" 
            ***Enter City Number***\n
            1. Middlesborough\n
            2. London\n
            3. Paris\n
            4. Toulouse\n """)
    while True:
        city_id = input('Select City Number:')
        if city_id.isdigit():
            city_id = int(city_id)
            if city_id >= 1 and city_id <= 4:
                city_query = f"SELECT name FROM cities WHERE id = {city_id}"
                connection = get_connection()
                cursor = connection.cursor()
                city_result = cursor.execute(city_query).fetchone()
                city_name = city_result[0]
                return (str(city_id),city_name)
        print('Enter a Valid City Nunber\n')
    

def get_year():
        conn = sqlite3.connect('../db/weather.db') 
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


def months_label():
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    return months