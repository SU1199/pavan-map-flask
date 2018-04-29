from flask import Flask, request, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import geocoder
import json
import urllib2
import requests

app = Flask(__name__, template_folder="templates")
app.config['GOOGLEMAPS_KEY'] = "AIzaSyCpr3HIBG54RcPBos-g-ihuy80VAJVLSPY" #api key
GoogleMaps(app) #initialise gmaps
# GoogleMaps(app, key="AIzaSyCpr3HIBG54RcPBos-g-ihuy80VAJVLSPY")
global o3 ,so2 , no2 ,pm10 ,pm25 , co
o3 = so2 = no2 = pm10 = pm25 = co = 0


@app.route('/')
def index():
   return render_template('index.html')


@app.route('/', methods=['POST'])
def usr_input():
    o3 = so2 = no2 = pm10 = pm25 = co = 0 #Could't find any elegant way
    a = b = c = d = e = f = False
    text = request.form['location']
    g = geocoder.google(text)
    lat = g.lat
    lng = g.lng    
    url ='https://api.openaq.org/v1/measurements?coordinates='+str(lat)+','+str(lng)+'&nearest=1'
    response = requests.get(url)
    data = response.json()
    length = len(data['results'])
    for i in range(0,length):
    	if data['results'][i]['parameter'] == 'so2' and a==False:
    		so2 = so2 + data['results'][i]['value']
    		a = True
    	elif data['results'][i]['parameter'] == 'no2' and b==False:
    		no2 = no2 + data['results'][i]['value']
    		b = True
    	elif data['results'][i]['parameter'] == 'co' and c==False:
    		co = co + data['results'][i]['value']
    		c = True
    	elif data['results'][i]['parameter'] == 'pm10' and d==False:
    		pm10 = pm10 + data['results'][i]['value']
    		d = True
    	elif data['results'][i]['parameter'] == 'pm25' and e==False:
    		pm25 = pm25 + data['results'][i]['value']
    		e = True
    	elif data['results'][i]['parameter'] == 'o3' and f==False:
    		o3 = o3 + data['results'][i]['value']
    		f = True

    data = data['results'][1]['parameter']
    return render_template(
        'map.html',
        lat=lat,
        lng=lng,
        data=data,
        no2=no2,
        so2=so2,
        co=co,
        pm10=pm10,
        pm25=pm25,
        o3=o3
    )

if __name__ == '__main__':
   app.run(debug = True)