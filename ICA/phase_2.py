from matplotlib import pyplot as plt 
from phase_1 import average_annual_temperature, average_mean_temp_by_city, average_seven_day_precipitation
from utils import get_city, get_date, get_connection, get_year,months_label

connection = get_connection()

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
    months = months_label()
    city = get_city()
    city_id = city[0]
    city_name = city[1]
    cursor = connection.cursor()  
    query = f"SELECT precipitation, mean_temp FROM daily_weather_entries WHERE city_id = {city_id} AND date BETWEEN '{year}-01-01' AND '{year}-12-31'"
    result = cursor.execute(query).fetchall()  
    presp, mean = zip(*result) 
    plt.plot(mean, label="Mean")
    plt.plot(presp, label="Precipitation")
    plt.legend()
    plt.xticks([])
    plt.title(f'{city_name} City mean temperature and Precipitation in the year {year}')
    plt.show()
  









