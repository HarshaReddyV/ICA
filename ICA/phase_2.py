from matplotlib import pyplot as plt 
from phase_1 import average_annual_temperature, average_mean_temp_by_city, average_seven_day_precipitation
from utils import get_city, get_date, get_connection, get_year

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
    query = f"SELECT date, mean_temp FROM [daily_weather_entries] WHERE date BETWEEN '{year}-01-01' AND '{year}-12-31' GROUP BY date "
    cursor = connection.cursor()
    result = cursor.execute(query).fetchall()
    print(result)
    pass






plot_meantemp_allcity_year()


