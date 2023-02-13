import os
import json
import folium
from folium.features import PolyLine
from mqtt_client import MqttClient
import random
from script import extractor
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

if firebase_admin._DEFAULT_APP_NAME in firebase_admin._apps:
    cred = credentials.Certificate('tank-gps-61f21-firebase-adminsdk-b4tyt-66f87b4637.json')
    default_app = firebase_admin.initialize_app(cred)
else:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'tank-gps-61f21-firebase-adminsdk-b4tyt-66f87b4637.json'
    f = open(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    firebaseConfig = json.load(f)
    cred = firebase_admin.credentials.Certificate(firebaseConfig)
    f.close()

# Import database module.

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://tank-gps-61f21-default-rtdb.firebaseio.com/'
})

ref = db.reference('gps')

def generate_distinct_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return f'#{r:02x}{g:02x}{b:02x}'

map_ = folium.Map(location=[23.794824, 90.414266], zoom_start=20)
'''
tracks = 
{
    "ID_1":
    {
        "location":[],
        "color":[]      
    }
}
'''
tracks = {}

extract = extractor('Dfmt01', 'Dfmt02', 'Dfmt03')

random.seed(69)

def extractLatLong(msg):
    global map_,tracks
    payload = str(msg.payload.decode('utf-8'))
    topic = msg.topic
    fmt, data = extract.__extract__(payload)
    
    if fmt == 'Dfmt01':
        print(data)
        ref.push(data)
    elif fmt == 'Dfmt02':
        if data["valid"] == '1':
            print(data)
            ref.push(data)
            if data["id"] not in tracks.keys():
                location = []
                color = generate_distinct_color()
                tracks[data["id"]] = {"location":location, "color":color}
                
            tracks[data["id"]]['location'].append((float(data["lat"]), float(data["long"])))
            
            for key in tracks.keys():
                
                PolyLine(locations=tracks[key]["location"], color=tracks[key]["color"], weight=5, opacity=0.7,
                        arrow_style='->').add_to(map_)
                
                marker = folium.Marker(tracks[key]["location"][-1], popup={"ID":key, "lat":tracks[key]["location"][-1][0], 
                                "long":tracks[key]["location"][-1][1]}, icon=None)
                
                marker.add_to(map_)
            
            map_.save('map.html')
            
            map_ = folium.Map(location=tracks[data["id"]]["location"][-1], zoom_start=20)
        else:
            print("Invalid GPS")

    elif fmt == "Dfmt03":
        print(data)
        ref.push(data)
    else:
        print("Invalid")


mqtt = MqttClient(id="0001")
mqtt.getMqttBroker("broker.hivemq.com")
mqtt.getMqttPort(1883)
mqtt.getMqttSubTopic("SD/GPS_Tracker")
mqtt.getMqttPubTopic("SD/GPS_Tracker")
mqtt.setOnMessageCallbackFunction(extractLatLong)

mqtt.connect()
mqtt.client.loop_forever()
