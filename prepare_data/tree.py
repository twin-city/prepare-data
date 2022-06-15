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

load_dotenv(Path(__file__).parents[1] / '.env')
CRS = "EPSG:2154"#lambert
inProj  = Proj(f"+init={CRS}",preserve_units=True)
outProj = Proj("+init=EPSG:4326") # WGS84 in degrees and not EPSG:3857 in meters)
# swap x,y as mkennedy says

data_path = Path(os.getenv('DATA_PATH'))


def get(url, quartier, force: bool=False) -> Path:

    path_json = data_path / 'les-arbres.json'

    dataset = 'les-arbres'
    quartier = [(649985, 6864006), (650266, 6864006),(650266, 6864226), (649985, 6864226),  (649985, 6864006)]

    polygon = ','.join([str(transform(inProj, outProj, x, y)[::-1]) for x,y in quartier])
    list_facet = '&facet=libellefrancais&facet=genre&facet=espece&facet=varieteoucultivar&facet=circonferenceencm&facet=hauteurenmf'

    url = url.format(dataset=dataset, polygon=polygon, list_facet=list_facet)

    if force or (not path_json.exists()):
        data_tree = requests.get(url)
        if data_tree.status_code == 200:
            write_json(path_json, data_tree.json())
            return data_tree.json()
        else:
            return data_tree.status_code

    elif path_json.exists():
        data = load(path_json)
        return data

def prepare(data_json: list, quartier):
    #data = load(path_json)

    data = pd.DataFrame.from_dict(data_json)
    arbres = pd.json_normalize(data['fields'])
    import pdb; pdb.set_trace()
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
