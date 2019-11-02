from flask import Flask
import sys
from flask_restful import Api, Resource, reqparse
import requests
import json
import datetime, time, calendar
import pandas as pd
import re

app = Flask(__name__)
api = Api(app)

darksky_api = "<your_api_key>"
geocode_api = "<your_api_key>"

def get_lat_long(city):
	response = requests.get(("https://maps.googleapis.com/maps/api/geocode/json?address="+str(city)+"&key="+geocode_api))
	latitude = response.json()['results'][0]['geometry']['location']['lat']
	longitude = response.json()['results'][0]['geometry']['location']['lng']
	return (latitude,longitude)

class Summary(Resource):

	def get(self, city):
		lat_long = get_lat_long(city)
		lat = str(lat_long[0])
		long = str(lat_long[1])
		current_time = datetime.datetime.now()
		unix_time = str(int(time.mktime(current_time.timetuple())))
		
		path = "./price.csv"
		rent_df = pd.read_csv(path)

		weather_data = requests.get("https://api.darksky.net/forecast/"+darksky_api+"/"+lat+","+long+","+unix_time)
		weather_json = weather_data.json()
		current_weather = weather_json.get('currently')

		summary = {}
		summary['city']=city

		if current_weather!=None:
			summary['temperature'] = current_weather.get('temperature')
			summary['rainfall'] = float(current_weather.get('precipIntensity'))
			summary['rainfall_probability'] = float(current_weather.get('precipProbability'))
			summary['current_weather']=current_weather.get('summary')
			summary['rent']='N/A'

			for index, row in rent_df.iterrows():
				if str(row['City'])==city:
					summary['rent']=float(row['January 2017'])
					break

		return json.dumps(summary), 200


class Average(Resource):

	def get(self, city, date):
		lat_long = get_lat_long(city)
		lat = str(lat_long[0])
		long = str(lat_long[1])
		month = int(date.split("-")[0])
		year = int(date.split("-")[1])
		num_days = calendar.monthrange(year, month)[1]
		days = [datetime.date(year, month, day) for day in range(1, num_days+1)]

		rain = 0.00
		temperature = 0.00
		avg_rain = 0.00
		avg_temp = 0.00


		for day in days:
			unix_time = str(int(time.mktime(day.timetuple())))
			
			weather_data = requests.get("https://api.darksky.net/forecast/"+darksky_api+"/"+lat+","+long+","+unix_time)

			precipIntensity = weather_data.json()['currently']['precipIntensity']
			temperature += float(weather_data.json()['currently']['temperature'])

			if precipIntensity!=0:
				precipType = weather_data.json()['currently']['precipType']
				if precipType=="rain" or precipType=="sleet":
					rain+=(float(precipIntensity)*24.00)

		avg_rain = (rain/num_days)*1.000
		avg_temp = (temperature/num_days)*1.000

		json_obj = {}

		json_obj['city']=city
		json_obj['month']=month
		json_obj['year']=year
		json_obj['avg_rain']=avg_rain
		json_obj['avg_temp']=avg_temp

		return json.dumps(json_obj)


class Rent(Resource):

	def get(self, rent):
		
		path = "./price.csv"
		rent_df = pd.read_csv(path)

		rent = int(rent)
		i = 0
		result_df = pd.DataFrame(columns=['City','Rent'])

		for index, row in rent_df.iterrows():
			if row['January 2017']<rent:
				new = pd.DataFrame({"City":row['City'], "Rent": row['January 2017']}, index=[i])
				i = i+1
				result_df = result_df.append(new)


		return result_df.to_json(orient='records'), 200

class Rent_Temperature(Resource):

	def get(self, rent, temp, date):

		temp = float(temp)
		rent = float(rent)

		forecasted_temp = None
		forecasted_weather = None

		date = re.sub('[-.:]', '/', date)
		date_obj = datetime.datetime.strptime(date, '%m/%d/%Y')
		unix_time = str(int(time.mktime(date_obj.timetuple())))

		path = "./price.csv"
		rent_df = pd.read_csv(path)

		i = 0

		cities=[]
		result_cities = []

		for index, row in rent_df.iterrows():
			if row['January 2017']<rent:
				cities.append(str(row['City']))

		for city in cities:

			#Limit the number of calls to Dark Sky API to a maximum of 100.
			i += 1
			if i>100:
				break

			lat_long = get_lat_long(city)
			lat = str(lat_long[0])
			long = str(lat_long[1])

			weather_data = requests.get("https://api.darksky.net/forecast/"+darksky_api+"/"+lat+","+long+","+unix_time)
			forecasted_weather = weather_data.json().get('currently')
			if forecasted_weather!=None:
				forecasted_temp = forecasted_weather.get('temperature')


			if forecasted_temp!=None:
				if forecasted_temp>=temp:
					result_cities.append(city)

		result = {}
		result['cities'] = result_cities
		print (len(cities), len(result_cities), file=sys.stdout)

		return json.dumps(result)

class Rent_Rainfall(Resource):

	def get(self, rent, rainfall, date):

		rainfall = float(rainfall)
		rent = float(rent)

		forecasted_rainfall = 0.00
		forecasted_weather = None

		date = re.sub('[-.:]', '/', date)
		date_obj = datetime.datetime.strptime(date, '%m/%d/%Y')
		unix_time = str(int(time.mktime(date_obj.timetuple())))

		path = "./price.csv"
		rent_df = pd.read_csv(path)

		i = 0

		cities=[]
		result_cities = []

		for index, row in rent_df.iterrows():
			if row['January 2017']<rent:
				cities.append(str(row['City']))

		for city in cities:

			#Limit the number of calls to Dark Sky API to a maximum of 100.
			i += 1
			if i>100:
				break

			lat_long = get_lat_long(city)
			lat = str(lat_long[0])
			long = str(lat_long[1])

			weather_data = requests.get("https://api.darksky.net/forecast/"+darksky_api+"/"+lat+","+long+","+unix_time)
			forecasted_weather = weather_data.json().get('currently')

			if forecasted_weather!=None:
				forecasted_rainfall = float(forecasted_weather.get('precipIntensity'))*24.00


			if forecasted_rainfall!=0:
				if forecasted_rainfall<=rainfall:
					result_cities.append(city)


		result = {}
		result['cities'] = result_cities

		return json.dumps(result)

api.add_resource(Summary, "/summary/<string:city>")
api.add_resource(Average, "/average/<string:city>,<string:date>")
api.add_resource(Rent, "/rent/<string:rent>")
api.add_resource(Rent_Temperature, "/rent/temperature/<string:rent>,<string:temp>,<string:date>")
api.add_resource(Rent_Rainfall, "/rent/rainfall/<string:rent>,<string:rainfall>,<string:date>")

if __name__=="__main__":
	app.run(debug=False)




