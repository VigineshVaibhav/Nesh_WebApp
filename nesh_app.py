from flask import Flask
from flask_restful import Api, Resource, reqparse
import requests
import json
import datetime, time, calendar
import pandas as pd

app = Flask(__name__)
api = Api(app)


def get_lat_long(city):
	response = requests.get(("https://maps.googleapis.com/maps/api/geocode/json?address="+str(city)+"&key=AIzaSyCNB2W8Z3zCJHDriis9G1AIOtHJ_h0aheQ"))
	latitude = response.json()['results'][0]['geometry']['location']['lat']
	longitude = response.json()['results'][0]['geometry']['location']['lng']
	return (latitude,longitude)


class Average_Rainfall(Resource):

	def get(self, city, month, year):
		lat_long = get_lat_long(city)
		lat = str(lat_long[0])
		long = str(lat_long[1])
		month = int(month)
		year = int(year)
		num_days = calendar.monthrange(year, month)[1]
		days = [datetime.date(year, month, day) for day in range(1, num_days+1)]

		rain = 0
		avg_rain = 0


		for day in days:
			unix_time = str(int(time.mktime(day.timetuple())))
			
			weather_data = requests.get("https://api.darksky.net/forecast/f50cf8c0dbdcd4d9e0e4948585b20362/"+lat+","+long+","+unix_time)
			print(weather_data.json())
			precipIntensity = weather_data.json()['currently']['precipIntensity']
			
			if precipIntensity!=0:
				precipType = weather_data.json()['currently']['precipType']
				if precipType=="rain" or precipType=="sleet":
					rain+=precipIntensity

		avg_rain = (rain/num_days)*1.000
		
		return "Average rainfall in " + str(city) + " on " + str(month) + "/" + str(year) + " is: " + str(avg_rain) + " (in inches)", 200

class Rent(Resource):

	def get(self, rent):
		
		path = "./price.csv"
		rent_df = pd.read_csv(path)

		rent = int(rent)
		i = 0
		result_df = pd.DataFrame(columns=['City','Rent (As of Jan 2017)'])

		for index, row in rent_df.iterrows():
			if row['January 2017']<=rent:
				new = pd.DataFrame({"City":row['City'], "Rent (As of Jan 2017)": row['January 2017']}, index=[i])
				i = i+1
				result_df = result_df.append(new)

		# data = {}

		# for index, row in result_df.iterrows():
		# 	data['City']=str(row['City'])
		# 	data['Rent (As of Jan 2017)'] = str(row['Rent (As of Jan 2017)'])

		return json.dumps(result_df.to_json(orient='records').replace("\'","")), 200


api.add_resource(Average_Rainfall, "/rainfall/<string:city>,<string:month>,<string:year>")
api.add_resource(Rent, "/rent/<string:rent>")

if __name__=="__main__":
	app.run(debug=True)




