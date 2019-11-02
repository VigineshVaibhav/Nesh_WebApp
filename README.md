# Nesh Backend Engineer Project Documentation
### Author: Viginesh Vaibhav
### Date Created: November 2, 2019

The API for this technical assessment is hosted on PythonAnywhere, at  [viginesh22.pythonanywhere.com](viginesh22.pythonanywhere.com). Here is a list of calls you can make to the API:

## 1. Get Current Summary Information of a City

*Syntax:* ``` viginesh22.pythonanywhere.com/summary/<city>```

*Example:* ```viginesh22.pythonanywhere.com/summary/Houston```

*Output:* A JSON object with the following attributes:

- city: City name
- temperature: current temperature of the city
- rainfall: Current rainfall level (in inches)
- rainfall_probability: Probability of rainfall (between 0 and 1, both inclusive)
- current_weather: Description of current weather in city ("Clear", "Overcast", etc.)
- rent: Rent value for city (as of Jan 2017)

## 2. Get Cities within Maximum Rent

*Syntax:* ``` viginesh22.pythonanywhere.com/rent/<max_rent>```

*Example:* ``` viginesh22.pythonanywhere.com/rent/1000```

Here, 'max_rent' is in dollars.

*Output:* An array of JSON objects, each of which has the following attributes:

- city: City name
- rent: Rent value for city (as of Jan 2017)

## 3. Get Average Rainfall and Temperature for a City on a Specific Month

*Syntax:* ```http://viginesh22.pythonanywhere.com/average/<city>,<mm-yyyy>```

*Example:* ```http://viginesh22.pythonanywhere.com/average/Houston,08-2017```

*Output:* A JSON object with the following attributes:

- city: City name
- month: Numeric value for the given month (between 1 to 12)
- year: Given year value
- avg_rain: City's average rainfall for the given month (in inches)
- avg_temp: City's average temperature for the given month (in Fahrenheit)

## 4. Get Cities within Maximum Rent and Minimum Temperature for a Given Date

*Syntax:* ```http://viginesh22.pythonanywhere.com/rent/temperature/<max_rent>,<min_temp>,<mm-dd-yyyy>```

*Example:* ```http://viginesh22.pythonanywhere.com/rent/temperature/750,50,01-01-2020```

Here, 'max_rent' is in dollars and 'min_temp' is in Fahrenheit.

*Output:* A JSON object with attribute 'cities', which contains a list of all city names which satisfy the given criteria for maximum rent and minimum temperature.


## 5. Get Cities within Maximum Rent and Maximum Rainfall for a Given Date

*Syntax:* ```http://viginesh22.pythonanywhere.com/rent/temperature/<max_rent>,<max_rainfall>,<mm-dd-yyyy>```

*Example:* ```http://viginesh22.pythonanywhere.com/rent/temperature/750,2.00,01-01-2020```

Here, 'max_rent' is in dollars and 'max_rainfall' is in inches.

*Output:* A JSON object with attribute 'cities', which contains a list of all city names which satisfy the given criteria for maximum rent and maximum rainfall.

### Important Note
For the 4<sup>th</sup> and 5<sup>th</sup> API calls described above, I've limited the number of calls to the Dark Sky API to 100. This is because the free tier only allows for 1000 calls a day. So the result will contain only a subset of all the cities that satisfy the given criteria.

In case you find that the API doesn't work or returns a 500 "Internal Server Error" message, it's most likely because the number of calls to Dark Sky's API has exceeded the daily limit of 1000 calls. In that case, please email me about this and I'll create a new API key for Dark Sky. Alternatively, you could wait for 24 hours to reset the number of calls made to the Dark Sky API, and then try again.


#### Thank you for giving me the opportunity to work on this project!
