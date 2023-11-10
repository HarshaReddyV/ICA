import sqlite3
from phase_1 import select_all_cities, select_all_countries, average_annual_temperature,average_mean_temp_by_city,average_annual_precipitation_by_country,average_seven_day_precipitation

connection = sqlite3.connect('../db/weather.db')

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
                return str(city_id)
                break
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



def main():
    print(""" 
        ******WELCOME****** \n
        Please Choose the option below to Navigate\n
        1. List All Countries information \n
        2. List All cities information\n
        3. Average Annual Temperature \n
        4. Average 7 Day Precipitation\n
        5. Average Mean Temperature of All Cities \n
        6. Average Annual Precepitation of Country \n 
        7. **EXIT** 
          """)
    while(True):
        choice = input('Enter the option Number: ')
        
        if choice.isdigit():
            choice = int(choice)
            if choice >= 1 and choice <= 7: 
                execute(choice)    
                break
        

def execute(choice):
    if choice == 1:
        select_all_countries(connection)
    elif choice == 2: 
        select_all_cities(connection)
    elif choice == 3:
        city_id = get_city()
        year = get_year()
        average_annual_temperature(connection, city_id,year)
    elif choice == 4:
        city_id = get_city()
        date = get_date()
        average_seven_day_precipitation(connection, city_id, date)       
    elif choice == 5:
        date_from = get_date()
        date_to = get_date()
        average_mean_temp_by_city(connection, date_from, date_to)
        pass
    elif choice == 6:
        year = get_year()
        average_annual_precipitation_by_country(connection, year)
        pass
    elif choice ==7:
        exit()


main()
