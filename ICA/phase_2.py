from matplotlib import pyplot as plt 
from phase_1 import average_annual_temperature, average_mean_temp_by_city, average_seven_day_precipitation
from utils import get_city, get_date, get_connection, get_year,months_label

connection = get_connection()

def plot_meantemp_allcity_date_range(): 
    date_from = get_date()
    date_to = get_date()
    data = average_mean_temp_by_city(date_from, date_to)
    cities, values = zip(*data)
    print(cities)
    print(values)
    plt.bar(cities, values, color='orange')
    plt.xlabel('Cities')
    plt.ylabel(f'Mean Temperature in \u00B0C')
    plt.title(f'Mean Temperature from {date_from} to {date_to}')
    plt.show()


def plot_meantemp_allcity_year():
    year = get_year()
    months = months_label()
    mid_query = f"SELECT date, mean_temp FROM [daily_weather_entries] WHERE date BETWEEN '{year}-01-01' AND '{year}-12-31' AND city_id = 1 "
    lon_query = f"SELECT date, mean_temp FROM [daily_weather_entries] WHERE date BETWEEN '{year}-01-01' AND '{year}-12-31' AND city_id = 2 "
    par_query = f"SELECT date, mean_temp FROM [daily_weather_entries] WHERE date BETWEEN '{year}-01-01' AND '{year}-12-31' AND city_id = 3 "
    tou_query = f"SELECT date, mean_temp FROM [daily_weather_entries] WHERE date BETWEEN '{year}-01-01' AND '{year}-12-31' AND city_id = 4 "
    cursor = connection.cursor()
    result = cursor.execute(mid_query).fetchall()
    date, mean = zip(*result)
    plt.plot(date,mean)
    plt.xticks([])
    plt.legend()
    plt.show()
    pass





plot_meantemp_allcity_year()


