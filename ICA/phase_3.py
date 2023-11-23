import sqlite3
from phase_1 import select_all_cities, select_all_countries, average_annual_temperature,average_mean_temp_by_city,average_annual_precipitation_by_country,average_seven_day_precipitation
from utils import get_city,get_date,get_year

connection = sqlite3.connect('../db/weather.db')

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
        select_all_countries()
    elif choice == 2: 
        select_all_cities()
    elif choice == 3:
        city_id = get_city()
        year = get_year()
        average_annual_temperature(city_id,year)
    elif choice == 4:
        city_id = get_city()
        date = get_date()
        average_seven_day_precipitation( city_id, date)       
    elif choice == 5:
        date_from = get_date()
        date_to = get_date()
        average_mean_temp_by_city( date_from, date_to)
        pass
    elif choice == 6:
        year = get_year()
        average_annual_precipitation_by_country(year)
        pass
    elif choice ==7:
        exit()


main()
