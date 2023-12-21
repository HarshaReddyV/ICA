import openmeteo_requests
import datetime
import requests_cache
import pandas as pd
from retry_requests import retry
from utils import get_connection, get_coordinates
# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 53.7965,
	"longitude": -1.5478,
	"daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
	"timezone": "GMT",
	"start_date": "2023-01-01",
	"end_date": f"{datetime.date.today()}"
}
responses = openmeteo.weather_api(url, params=params)
# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
# Process daily data. The order of variables needs to be the same as requested.
daily = response.Daily()
daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
daily_precipitation_sum = daily.Variables(2).ValuesAsNumpy()

daily_data = {"date": pd.date_range(
	start = pd.to_datetime(daily.Time(), unit = "s"),
	end = pd.to_datetime(daily.TimeEnd(), unit = "s"),
	freq = pd.Timedelta(seconds = daily.Interval()),
	inclusive = "left"
)}
daily_data["temperature_2m_max"] = daily_temperature_2m_max
daily_data["temperature_2m_min"] = daily_temperature_2m_min
daily_data["precipitation_sum"] = daily_precipitation_sum

#Inserting the data into database 
conn = get_connection()
cursor = conn.cursor()

for i in range(len(daily_data['date'])):	
	max_temp = daily_data['temperature_2m_max'][i]
	min_temp = daily_data['temperature_2m_min'][i]
	precp = daily_data['precipitation_sum'][i]
	mean_temp = (max_temp + min_temp)/2
    
	#Formating data for inserting into database
	date = daily_data['date'][i].strftime('%Y-%m-%d')
	max_temp = f'{max_temp: .2f}'
	min_temp = f'{min_temp: .2f}'
	mean_temp = f'{mean_temp:.2f}'
	precp = f'{precp:.2f}'
    
	#Deleting any existing data to avoid duplication
	query = f"DELETE FROM daily_weather_entries WHERE strftime('%Y', date) = '2023'"
	cursor.execute(query)
	conn.commit()

    #Inserting data into database
	query = f"INSERT INTO daily_weather_entries (date, min_temp, max_temp, mean_temp, precipitation, city_id) VALUES ('{date}', '{min_temp}', '{max_temp}', '{mean_temp}', '{precp}', '5')"
	cursor.execute(query)
	conn.commit()






def add_new_city():
	#Getting coordinates from city name
	while True:
		city_name = input('Enter City Name:').strip()
		if city_name.isalpha():
			coordinates = get_coordinates(city_name)
			print(coordinates[0],coordinates[1])
		else:
			print('Enter a valid city name')
    
	#Checking the name doesn't exists in database
    

