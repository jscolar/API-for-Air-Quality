from flask import Flask, render_template, request, jsonify
import plotly.graph_objs as go
from plotly.utils import PlotlyJSONEncoder
import json
import requests
import requests_cache
from pprint import pprint

requests_cache.install_cache('air_api_cache', backend='sqlite', expire_after=36000)


app = Flask(__name__, instance_relative_config = True)
app.config.from_object('config')
app.config.from_pyfile('config.py')


air_url_template = 'https://api.breezometer.com/air-quality/v2/historical/hourly?lat={lat}&lon={lng}&key={API_Key}&start_datetime={start}&end_datetime={end}'


@app.route('/airqualitychart',  methods=['GET'])
def airchart():
    my_latitude = request.args.get('lat','51.52369')
    my_longitude = request.args.get('lng','-0.0395857')
    my_start = request.args.get('start','2019-02-22T07:00:00Z')
    my_end = request.args.get('end','2019-02-25T07:00:00Z')


    air_url = air_url_template.format(lat = my_latitude, lng = my_longitude, API_Key = app.config['MY_API_KEY'], start = my_start, end = my_end)

    resp = requests.get(air_url)

    if resp.ok:
        airquality=resp.json()
        pprint(airquality)

    else:
        print(resp.reason)

    return ("Good job baby!")

if __name__=="__main__":
    app.run(port=8080, debug=True)
