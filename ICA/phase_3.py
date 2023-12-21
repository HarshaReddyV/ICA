import sqlite3
import time
from phase_1 import select_all_cities, select_all_countries, average_annual_temperature,average_mean_temp_by_city,average_annual_precipitation_by_country,average_seven_day_precipitation
from utils import get_city,get_date,get_year
from phase_2 import plot_mean_month_city,plot_mean_temp_yearly,plot_meantemp_allcity_date_range,plot_precp_month_city,plot_temp_precep_city_year
from phase_4 import add_new_city,update_data
connection = sqlite3.connect('../db/weather.db')

def main(): 
    while(True):
        print(""" 
        ******WELCOME****** \n
        Please Choose the option below to Navigate\n
        1. List All Countries information \n
        2. List All cities information\n
        3. Average Annual Temperature \n
        4. Average 7 Day Precipitation\n
        5. Average Mean Temperature of All Cities \n
        6. Average Annual Precepitation of Country \n
        7. Plot Mean temperature for city by month\n
        8. Plot Mean temperature by month\n
        9. Plot Mean temperature for City by Date Range \n
        10. Plot precepitation for city by month\n
        11. Plot Mean temperature and precepitation for city by year \n
        12. Add new City into database \n
        13. Update Database with latest data (2023) \n
        14. **EXIT** 
        """)
        choice = input('Enter the option Number: ')
        
        if choice.isdigit():
            choice = int(choice)
            if choice >= 1 and choice <= 13: 
                execute(choice)
                print('Main Menu will be displayed shortly...')    
                time.sleep(5)
        

def execute(choice):
    if choice == 1:
        select_all_countries()
    elif choice == 2: 
        select_all_cities()
    elif choice == 3:
        city_result = get_city()
        city_id = city_result[0]
        year = get_year()
        average_annual_temperature(city_id,year)
    elif choice == 4:
        city_result = get_city()
        city_id = city_result[0]
        date = get_date()
        average_seven_day_precipitation( city_id, date)       
    elif choice == 5:
        date_from = get_date()
        date_to = get_date()
        average_mean_temp_by_city( date_from, date_to)
    elif choice == 6:
        year = get_year()
        average_annual_precipitation_by_country(year)
    elif choice ==7:
        plot_mean_month_city()
    elif choice == 8:
        plot_mean_temp_yearly()
    elif choice ==9:
        plot_meantemp_allcity_date_range()
    elif choice == 10:
        plot_precp_month_city()
    elif choice == 11:
        plot_temp_precep_city_year()
    elif choice == 12:
        add_new_city()
    elif choice == 13:
        update_data()
    elif choice == 14: 
        exit()


main()
