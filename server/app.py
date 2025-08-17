from flask import Flask , jsonify
import openmeteo_requests
import pandas as pd
import requests_cache
from datetime import datetime , timezone
from retry_requests import retry
from flask_cors import CORS , cross_origin


#from the meteo API that ensures the api is works and retries on errors
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)


base_url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 39.1149995,
	"longitude": -94.6268,
	"hourly": "temperature_2m",
	"timezone": "America/Chicago",
	"wind_speed_unit": "mph",
	"temperature_unit": "fahrenheit",
}
responses = openmeteo.weather_api(base_url, params=params)
loc_reponse = responses[0]

#all the hourly times
hourly = loc_reponse.Hourly()

start_time = datetime.fromtimestamp(hourly.Time() , tz=timezone.utc)


temps = hourly.Variables(0).ValuesAsNumpy()
interval = hourly.Interval()
the_utc = datetime.now(timezone.utc)




app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "http://localhost:3000"]}})



#this will be the method that gives us the hourly for the next 8 hours
@app.route("/index")
def index():
    current_hour = int((the_utc - start_time).total_seconds()/hourly.Interval())

    
    hourly_temps = [int(temps[current_hour])]

    for i in range(7):
        hourly_temps.append(int(temps[current_hour + (i + 1)]))

    
    return hourly_temps


@app.route("/temp-time")
@cross_origin(origin="http://localhost:5173")
def cur_temp_time():
    timezone = loc_reponse.Timezone().decode("utf-8")
    current_time = datetime.now()
    hours_since_start = int((the_utc - start_time).total_seconds() / hourly.Interval())

    #starter want to make it return state of weather and change this method to one section
    temp_time = {"temperature" : int(temps[hours_since_start]) , "time" : current_time , "timezone" : timezone }
    


    return jsonify(temp_time)



#this method should access the next couple of days of weather and provide the lowest/highest temps 
@app.route("/upcoming-weather")
def upcoming_weather():
    day_to_skip = 24    
    cur_skip = 1

    goal = {"dayOne": [] , "dayTwo" : [] , "dayThree" : []}

    while cur_skip <= 3:
        all_temps_for_day = []
        first_last_temp = []
        for i in range(24):
            all_temps_for_day.append(int(temps[i + day_to_skip]))

        all_temps_for_day.sort()

        first_last_temp.append(all_temps_for_day[0])
        first_last_temp.append(all_temps_for_day[23])


        if cur_skip == 1:
            goal["dayOne"] = first_last_temp
        elif cur_skip == 2:
            goal["dayTwo"] = first_last_temp
        else:
            goal["dayThree"] = first_last_temp

        cur_skip += 1
        day_to_skip += 24

    return jsonify(goal)
    

if __name__ == "__main__":
    app.run(debug=True)