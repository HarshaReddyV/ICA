from matplotlib import pyplot as plt 
from phase_1 import average_annual_temperature, average_mean_temp_by_city, average_seven_day_precipitation
from utils import get_city, get_date, get_connection, get_year, get_month

connection = get_connection()
cursor = connection.cursor()

def plot_meantemp_allcity_date_range(): 
    date_from = get_date()
    date_to = get_date()
    data = average_mean_temp_by_city(date_from, date_to)
    cities, values = zip(*data)
    plt.bar(cities, values, color='orange')
    plt.xlabel('Cities')
    plt.ylabel(f'Mean Temperature in \u00B0C')
    plt.title(f'Mean Temperature from {date_from} to {date_to}')
    plt.show()


def plot_temp_precep_city_year():
    year = get_year()
    city = get_city()
    city_id = city[0]
    city_name = city[1]  
    query = f"SELECT precipitation, mean_temp FROM daily_weather_entries WHERE city_id = {city_id} AND date BETWEEN '{year}-01-01' AND '{year}-12-31'"
    result = cursor.execute(query).fetchall()  
    presp, mean = zip(*result) 
    plt.plot(mean, label="Mean")
    plt.plot(presp, label="Precipitation")
    plt.legend()
    plt.xticks([])
    plt.title(f'{city_name} City mean temperature and Precipitation in the year {year}')
    plt.show()
  

def plot_mean_month_city():
    year = get_year()
    city = get_city()
    city_id = city[0]
    city_name = city[1]
    result_month = get_month()
    month_id = result_month[0]
    month_name = result_month[1]   
    query = f"SELECT  date, mean_temp FROM daily_weather_entries WHERE strftime('%Y', date) = '{year}' AND strftime('%m', date) = '{month_id}' AND city_id = '{city_id}' "
    results = cursor.execute(query).fetchall()
    if len(results) == 0:
        print('Data is not available, Please try with different date range')
        exit()
    else:
        date, result = zip(*results)
        plt.plot(date, result, label="Monthly Mean Temperature by City")
        plt.xticks(rotation = 90)
        plt.title(f"Mean Temperature in {city_name} in {month_name},{year}")
        plt.show()


def plot_precp_month_city():
    year = get_year()
    city = get_city()
    city_id = city[0]
    city_name = city[1]
    result_month = get_month()
    month_id = result_month[0]
    month_name = result_month[1]
    query = f"SELECT  date, precipitation FROM daily_weather_entries WHERE strftime('%Y', date) = '{year}' AND strftime('%m', date) = '{month_id}' AND city_id = '{city_id}' "
    results = cursor.execute(query).fetchall()
    if len(results) == 0:
        print('Data is not available, Please try with different date range')
        exit()
    else:
        date, result = zip(*results)
        plt.plot(date, result, label="Monthly Precipitation by City")
        plt.xticks(rotation = 90)
        plt.title(f"Precipitation in {city_name} in {month_name},{year}")
        plt.show()
    

def plot_mean_temp_yearly():
    year = get_year()
    query = f"SELECT c.name, d.mean_temp FROM daily_weather_entries d JOIN cities c WHERE d.city_id == c.id AND d.date BETWEEN '{year}-01-01' AND '{year}-12-31' GROUP BY c.name"
    results = cursor.execute(query).fetchall()
    print(results)
    city, mean = zip(*results)
    plt.bar(city,mean, label=f"Yearly Mean Temperature in {year}", color="green")
    plt.title(f"Yearly City Mean Temperature in {year}")
    plt.show()
    



plot_mean_temp_yearly()

    







