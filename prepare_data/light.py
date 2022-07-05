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
from utils import load, write as write_json
from math import nan

load_dotenv(Path(__file__).parents[1] / '.env')
CRS = "EPSG:2154"#lambert
inProj  = Proj(f"+init={CRS}",preserve_units=True)
outProj = Proj("+init=EPSG:4326") # WGS84 in degrees and not EPSG:3857 in meters)
# swap x,y as mkennedy says
data_path = Path(os.getenv('DATA_PATH'))

def get(url, quartier, force: bool=False) -> Path:
    dataset = 'eclairage-public'
    path_json = data_path / f'{dataset}.json'
    columns = ['lib_suppor', 'hauteur_su']
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
        data_light = requests.get(url)
        if data_light.status_code == 200:
            write_json(path_json, data_light.json())
            return data_light.json()
        else:
            return data_light.status_code

    if path_json.exists():
        data = load(path_json)
        return data

def prepare(data_json: list):
    #data = load(path_json)
    data = pd.DataFrame.from_dict(data_json['records'])
    lights = pd.json_normalize(data['fields'])
    lights = lights[['lib_suppor', 'hauteur_su', 'geo_point_2d']]
    lights.rename(columns={'lib_suppor':'support', 'hauteur_su':'hauteur'}, inplace= True)
    lights=lights.replace({nan: None})
    coordonnees=[]
    index_to_remove=[]
    repere = ['x','y']
    for i, row in lights.iterrows():
        coordonnees.append(row['geo_point_2d'][::-1])

    for i in range(len(coordonnees)):
        coordonnees[i] = dict(zip(repere, coordonnees[i]))

    lights['coordonnees'] = coordonnees
    lights.drop('geo_point_2d', axis='columns', inplace=True)
    lights.drop(axis=0, index = index_to_remove, inplace = True)
    data_lights = pd.DataFrame(lights)

    return {'data': data_lights.to_dict(orient='records')}

def write(path_lights: Path, data, force=True):
    if force or (not path_lights.exists()):
        write_json(path_lights, data)
