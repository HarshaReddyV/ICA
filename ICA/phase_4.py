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

#db connection
conn = get_connection()
cursor = conn.cursor()

#Deleting any existing data to avoid duplication
def clean_db():
	query = f"DELETE FROM daily_weather_entries WHERE strftime('%Y', date) = '2023'"
	cursor.execute(query)
	conn.commit()
	print('Existing data has been cleared..for 2023\n') 
	print('**** The data for 2023 is skewed and not available for Jan to June for all cities and is not accurate although successfully retrieved.... Continuing as this is not core requirment ****\n')
	


def api_call(city_id,longitude,latitude):
	url = "https://api.open-meteo.com/v1/forecast"
	params = {
		"latitude": f'{latitude}',
		"longitude": f'{longitude}',
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
		
		#Inserting data into database
		query = f"INSERT INTO daily_weather_entries (date, min_temp, max_temp, mean_temp, precipitation, city_id) VALUES ('{date}', '{min_temp}', '{max_temp}', '{mean_temp}', '{precp}', '{city_id}')"
		cursor.execute(query)
		conn.commit()


def update_data():
	clean_db()
	query = "SELECT id,name,longitude,latitude FROM cities"
	results = cursor.execute(query).fetchall()
	for result in results:
		city_id = result[0]
		city_name = result[1]
		longitude = result[2]
		latitude = result[3]
		api_call(city_id,longitude,latitude)
		print(f'{city_name} has been updated with 2023 weather data\n')
	
def add_new_city():
	#Getting coordinates from city name
	while True:
		city_name = input('Enter City Name:').strip().lower()
		if city_name.isalpha():
			coordinates = get_coordinates(city_name)
			latitude = coordinates[0]
			longitude = coordinates[1]
			break
		else:
			print('Enter a valid city name')
			continue
    
	#Checking the name doesn't exists in database and adding into db
	query = "SELECT DISTINCT name FROM cities"
	results = cursor.execute(query).fetchall()
	results = [result[0].lower() for result in results]
	
	if city_name in results:
		print('City Name has already been added to database, try updating the data from main menu')
	else:
		query = f"INSERT INTO cities(name,longitude,latitude,country_id) VALUES('{city_name.capitalize()}','{longitude}','{latitude}','3')"
		#query = f"DELETE FROM cities WHERE country_id =3"
		cursor.execute(query)
		conn.commit()
		print('City Has been added successfully..!')

