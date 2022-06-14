import requests
import pandas as pd
import json
import requests
from pathlib import Path
import geopandas as gpd
import geojson
import shapely
from shapely.geometry import Polygon, LineString, MultiLineString, MultiPolygon, collection, Point

def get(url):
    data_tree = requests.get(url)
    if data_tree.status_code == 200:
        return data_tree.json()
    else:
        return data_tree.status_code

def save(data, path:Path):
    data_arbres = json.dumps(data)
    with open(path, 'w') as outfile:
        outfile.write(data_arbres)

def prepare(data):
    data = pd.DataFrame.from_dict(data)
    arbres = pd.json_normalize(data['fields'])
    arbres = arbres[['hauteurenm', 'libellefrancais', 'geo_point_2d']]
    arbres.rename(columns={'hauteurenm':'hauteur', 'libellefrancais':'espece'})

    quartier = Polygon([(649985, 6864006), (650266, 6864006),(650266, 6864226), (649985, 6864226),  (649985, 6864006)])
    coordonnees=[]
    index_to_remove=[]
    repere = ['x','y']
    for i, row in arbres.iterrows():
        coordonnees.append(row['geo_point_2d'][::-1])
        point = Point(row['geo_point_2d'][1], row['geo_point_2d'][0])
        if not quartier.contains(point):
            index_to_remove.append(i)
    
    for i in range(len(coordonnees)):
        coordonnees[i] = dict(zip(repere, coordonnees[i]))

    arbres['coordonnees']=coordonnees
    arbres.drop('geo_point_2d', axis='columns', inplace=True)
    arbres.drop(axis=0, index = index_to_remove, inplace = True)
    data_arbres = pd.DataFrame(arbres)
    return data_arbres

def write(data):
    data.to_json('/workspace/home/data/arbres_place_st_augustin.json', orient = "table")