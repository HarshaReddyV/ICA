from matplotlib import pyplot as plt 

from phase_1 import average_annual_temperature, average_mean_temp_by_city, average_seven_day_precipitation
from utils import get_city, get_date

def plot_average_city_mean_temperature(): 
    date_from = get_date()
    date_to = get_date()
    data = average_mean_temp_by_city(date_from, date_to)
    cities, values = zip(*data)
    print(cities)
    print(values)
    plt.bar(cities, values, color='orange')
    plt.xlabel('Cities')
    plt.ylabel(f'Mean Temperature in ^oc ')
    plt.title(f'Mean Temperature from {date_from} to {date_to}')
    plt.show()


plot_average_city_mean_temperature()