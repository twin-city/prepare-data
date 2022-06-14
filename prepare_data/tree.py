import requests
import pandas as pd
import json, os
import requests
from pathlib import Path
import geopandas as gpd
import geojson
import shapely
from shapely.geometry import Polygon, LineString, MultiLineString, MultiPolygon, collection, Point
from dotenv import load_dotenv
from utils import load, write as write_json

load_dotenv(Path(__file__).parents[1] / '.env')
CRS = "EPSG:2154"#lambert
data_path = Path(os.getenv('DATA_PATH'))

def get(url, force: bool=False) -> Path:

    path_json = data_path / 'les-arbres.json'
    if force or (not path_json.exists()):
        data_tree = requests.get(url)
        if data_tree.status_code == 200:
            write_json(path_json, data_tree.json())
            return path_json
        else:
            return data_tree.status_code

    return path_json

def prepare(path_json: Path, quartier):
    #data = load(path_json)
    #import pdb; pdb.set_trace()
    data = pd.read_json(path_json)
    arbres = pd.json_normalize(data['fields'])
    arbres = arbres[['hauteurenm', 'libellefrancais', 'geo_point_2d']]
    arbres.rename(columns={'hauteurenm':'hauteur', 'libellefrancais':'espece'})

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
    return data_arbres.to_dict()

def write(path_tree: Path, data, force=True):
    if force or (not path_tree.exists()):
        data.to_json(path_tree, orient = "table")
