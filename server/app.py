from flask import Flask
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

#from the meteo API that ensures the api is works and retries on errors
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)


base_url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 39.1149995,
	"longitude": 94.6268,
	"hourly": "temperature_2m",
	"timezone": "America/Chicago",
}
responses = openmeteo.weather_api(base_url, params=params)
loc_reponse = responses[0]




app = Flask(__name__)




@app.route("/index")
def index():
    timezone = loc_reponse.Timezone().decode("utf-8")
    
    return f"{loc_reponse.Latitude()} and {loc_reponse.Longitude()} at {timezone}"

if __name__ == "__main__":
    app.run(debug=True)