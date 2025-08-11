from flask import Flask , jsonify
import openmeteo_requests
import pandas as pd
import requests_cache
from datetime import datetime , timezone
from retry_requests import retry



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
hourly = loc_reponse.Hourly()
start_time = datetime.fromtimestamp(hourly.Time() , tz=timezone.utc)
temps = hourly.Variables(0).ValuesAsNumpy()
interval = hourly.Interval()
the_utc = datetime.now(timezone.utc)




app = Flask(__name__)




@app.route("/index")
def index():
    
    return "completed dictionary for temp / time"

@app.route("/temp-time")
def cur_temp_time():
    timezone = loc_reponse.Timezone().decode("utf-8")
    current_time = datetime.now()
    hours_since_start = int((the_utc - start_time).total_seconds() / hourly.Interval())

    #starter want to make it return state of weather and change this method to one section
    temp_time = {"tempature" : temps[hours_since_start] , "time" : current_time , "timezone" : timezone }

    return str(temp_time)



#this method should access the next couple of days of weather and provide the lowest/highest temps 
def upcoming_weather():
    
    return ""
    

if __name__ == "__main__":
    app.run(debug=True)