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
from pyproj import Proj, transform
from math import nan

from .utils import load, write as write_json

load_dotenv(Path(__file__).parents[1] / '.env')
CRS = "EPSG:2154"#lambert
inProj  = Proj(f"+init={CRS}",preserve_units=True)
outProj = Proj("+init=EPSG:4326") # WGS84 in degrees and not EPSG:3857 in meters)
# swap x,y as mkennedy says
data_path = Path(os.getenv('DATA_PATH'))

def get(url, quartier, force: bool=False) -> Path:

    path_json = data_path / 'bollard.json'
    dataset = 'plan-de-voirie-mobiliers-urbains-bornes-barrieres-potelets'
    columns = ['lib_level']
    rows = 1000
    #quartier = [(649985, 6864006), (650266, 6864006),(650266, 6864226), (649985, 6864226),  (649985, 6864006)]
    quartier = [(x,y) for x,y in zip(*quartier.exterior.coords.xy)]
    polygon = ','.join([str(transform(inProj, outProj, x, y)[::-1]) for x,y in quartier])
    list_facet = '&'.join(['facet=' + col for col in columns])
    url = url.format(dataset=dataset,
                    polygon=polygon,
                    list_facet=list_facet,
                    rows=rows)

    if force or (not path_json.exists()):
        data_bollard = requests.get(url)
        if data_bollard.status_code == 200:
            write_json(path_json, data_bollard.json())
            return data_bollard.json()
        else:
            return data_bollard.status_code

    elif path_json.exists():
        data = load(path_json)
        return  data

def prepare(data_json: list):
    #data = load(path_json)
    data = pd.DataFrame.from_dict(data_json['records'])
    if 'fields' not in data:
        return {'data': []}
    bollards = pd.json_normalize(data['fields'])
    bollards = bollards[['lib_level', 'geo_point_2d']]
    bollards.rename(columns={'lib_level':'type'}, inplace= True)
    bollards=bollards.replace({nan: None})
    coordonnees=[]
    index_to_remove=[]
    repere = ['x','y']
    for i, row in bollards.iterrows():
        coordonnees.append(row['geo_point_2d'][::-1])

    for i in range(len(coordonnees)):
        coordonnees[i] = dict(zip(repere, coordonnees[i]))

    bollards['coordonnees']=coordonnees
    bollards.drop('geo_point_2d', axis='columns', inplace=True)
    bollards.drop(axis=0, index = index_to_remove, inplace = True)
    data_bollards = pd.DataFrame(bollards)
    return {'data' : data_bollards.to_dict(orient='records')}

def write(path_bollards: Path, data, force=True):
    if force or (not path_bollards.exists()):
        write_json(path_bollards, data)
