
from flask import Flask, render_template
import folium
import pandas as pd
import geopandas as gpd
import requests
import http.client
import json
import requests
from pandas import json_normalize
import pandas as pd
import numpy as np
import folium
import json
import folium
import geopandas as gpd
import numpy as np
import pandas as pd
from folium import Figure, IFrame, plugins
from folium.plugins import DualMap, HeatMap, MarkerCluster
from shapely import wkt



app = Flask(__name__)
@app.route("/")


def index():
    render_template('template.html')


    # URL for Barcelona Neighborhoods data for mapping
    url_barris = "https://opendata-ajuntament.barcelona.cat/data/dataset/808daafa-d9ce-48c0-925a-fa5afdb1ed41/resource/b21fa550-56ea-4f4c-9adc-b8009381896e/download"
    barri_geo_df=pd.read_csv(url_barris)

    barri_geo_df['geometry'] = barri_geo_df['geometria_wgs84'].apply(wkt.loads)
    barri_geo_df = gpd.GeoDataFrame(barri_geo_df, crs='epsg:4326')

    barri_geo_df.rename(columns={'codi_barri': 'Codi_Barri'}, inplace=True)
    barri_geo_df.rename(columns={'nom_barri': 'Nom_Barri'}, inplace=True)

    barri_geo_df = barri_geo_df.drop(['geometria_etrs89', 'geometria_wgs84', 'codi_districte'], axis=1)

    json_barri_geo = barri_geo_df.to_json()

    json_barri_geo

    def convert_to_geojson(data):
        features = []
        for record in data['result']['records']:
            try:
                latitude = float(record['geo_epgs_4326_x'])
                longitude = float(record['geo_epgs_4326_y'])
                feature = {
                    'type': 'Feature',
                    'properties': record,  # Add all record data as properties
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [longitude, latitude]
                    }
                }
                features.append(feature)
            except (ValueError, KeyError):
                # Skip records with missing or invalid coordinates
                continue

        geojson = {
            'type': 'FeatureCollection',
            'features': features
        }

        return geojson


    connect_opendata = http.client.HTTPSConnection("opendata-ajuntament.barcelona.cat")

    headers = {
        'cache-control': "no-cache"
        }

    connect_opendata.request("GET", "https://opendata-ajuntament.barcelona.cat/data/api/action/datastore_search?resource_id=e0779edc-8e62-4024-887b-07bf9e169661", headers=headers)

    response = connect_opendata.getresponse()
    data = response.read()

    json_data = json.loads(data)


    mercatsifires_geo_json = convert_to_geojson(json_data)


    # Modifying the GeoJSON data to keep only the specified keys in the properties and all geometry data

    # Specified properties to keep
    properties_to_keep = {
        'addresses_district_id',
        'addresses_district_name',
        'addresses_neighborhood_id',
        'addresses_neighborhood_name',
        'name'
    }

    # Updating each feature in the GeoJSON data
    for feature in mercatsifires_geo_json["features"]:
        feature["properties"] = {key: feature["properties"][key] for key in properties_to_keep}

    # The modified GeoJSON data is now ready
    mercatsifires_geo_json = mercatsifires_geo_json


    connect_opendata = http.client.HTTPSConnection("opendata-ajuntament.barcelona.cat")

    headers = {
        'cache-control': "no-cache"
        }

    connect_opendata.request("GET", "https://opendata-ajuntament.barcelona.cat/data/api/action/datastore_search?resource_id=9caf3470-f325-4079-9884-8bc819104884", headers=headers)

    response = connect_opendata.getresponse()
    data = response.read()

    json_data = json.loads(data)

    mercatsmun_geo_json = convert_to_geojson(json_data)

    # Modifying the GeoJSON data to keep only the specified keys in the properties and all geometry data

    # Specified properties to keep
    properties_to_keep = {
        'addresses_district_id',
        'addresses_district_name',
        'addresses_neighborhood_id',
        'addresses_neighborhood_name',
        'name'
    }

    # Updating each feature in the GeoJSON data
    for feature in mercatsmun_geo_json["features"]:
        feature["properties"] = {key: feature["properties"][key] for key in properties_to_keep}

    # The modified GeoJSON data is now ready
    mercatsmun_geo_json = mercatsmun_geo_json


    connect_opendata = http.client.HTTPSConnection("opendata-ajuntament.barcelona.cat")

    headers = {
        'cache-control': "no-cache"
        }

    connect_opendata.request("GET", "https://opendata-ajuntament.barcelona.cat/data/api/action/datastore_search?resource_id=d9153b84-2694-4c4f-8805-c861d4e98863", headers=headers)

    response = connect_opendata.getresponse()
    data = response.read()

    json_data = json.loads(data)

    granscentres_geo_json = convert_to_geojson(json_data)

    # Modifying the GeoJSON data to keep only the specified keys in the properties and all geometry data

    # Specified properties to keep
    properties_to_keep = {
        'addresses_district_id',
        'addresses_district_name',
        'addresses_neighborhood_id',
        'addresses_neighborhood_name',
        'name'
    }

    # Updating each feature in the GeoJSON data
    for feature in granscentres_geo_json["features"]:
        feature["properties"] = {key: feature["properties"][key] for key in properties_to_keep}

    # The modified GeoJSON data is now ready
    granscentres_geo_json = granscentres_geo_json



    connect_opendata = http.client.HTTPSConnection("opendata-ajuntament.barcelona.cat")

    headers = {
        'cache-control': "no-cache"
        }

    connect_opendata.request("GET", "https://opendata-ajuntament.barcelona.cat/data/api/action/datastore_search?resource_id=bdfb9d2f-4f72-43d4-bcb9-760523c74917", headers=headers)

    response = connect_opendata.getresponse()
    data = response.read()

    json_data = json.loads(data)

    galeries_geo_json = convert_to_geojson(json_data)

    # Modifying the GeoJSON data to keep only the specified keys in the properties and all geometry data

    # Specified properties to keep
    properties_to_keep = {
        'addresses_district_id',
        'addresses_district_name',
        'addresses_neighborhood_id',
        'addresses_neighborhood_name',
        'name'
    }

    # Updating each feature in the GeoJSON data
    for feature in galeries_geo_json["features"]:
        feature["properties"] = {key: feature["properties"][key] for key in properties_to_keep}

    # The modified GeoJSON data is now ready
    galeries_geo_json = galeries_geo_json

    # Function to add GeoJSON points to the map with custom icons
    def add_geojson_points(map_object, geojson_data, icon_url, layer_name):
        for feature in geojson_data['features']:
            if feature['geometry']['type'] == 'Point':
                coordinates = feature['geometry']['coordinates']
                folium.Marker(
                    location=[coordinates[1], coordinates[0]], 
                    icon=folium.features.CustomIcon(icon_url, icon_size=(20, 20)),
                    popup=feature['properties']['name']  # Assuming 'name' is a property
                ).add_to(map_object)


    # Create map
    barcelona_coords = [41.386, 2.19]
    map_bcn = folium.Map(location=barcelona_coords,tiles='CartoDB positron', zoom_start=11.5)

    icon_url_1 = "https://cdn-icons-png.flaticon.com/512/7618/7618214.png"
    icon_url_2 = "https://cdn-icons-png.flaticon.com/512/998/998718.png"
    icon_url_3 = "https://cdn-icons-png.flaticon.com/512/862/862856.png"
    icon_url_4 = "https://cdn.iconscout.com/icon/premium/png-256-thumb/farmers-market-4278873-3556437.png?f=webp"


    # Add each GeoJSON layer (replace icon URLs with your own)
    add_geojson_points(map_bcn, galeries_geo_json, icon_url_1, 'Galeries')
    add_geojson_points(map_bcn, granscentres_geo_json, icon_url_2, 'Grans Centres')
    add_geojson_points(map_bcn, mercatsmun_geo_json, icon_url_3, 'Mercats Municipals')
    add_geojson_points(map_bcn, mercatsifires_geo_json, icon_url_4, 'Mercats i Fires')

    # Style function for polygons
    style_function = lambda x: {
        'fillColor': '#FFA07A',  # Light orange color
        'color': '#000000',      # Border color
        'fillOpacity': 0.7,
        'weight': 1
    }

    # Adding the polygon layer (assuming barri_geo_df is your polygon data)
    folium.GeoJson(
        data=barri_geo_df,
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(
            fields=['Nom_Barri'],
            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
        )
    ).add_to(map_bcn)
    return map_bcn._repr_html_()

if __name__ == "__main__":
    app.run()



