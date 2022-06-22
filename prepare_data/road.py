import os
import pandas as pd
import geopandas as gpd
import geojson
import json
import shapely
from shapely.geometry import Polygon, LineString, MultiLineString, MultiPolygon, collection
from pathlib import Path
import requests
from geojson import Polygon
import py7zr
import re
from dotenv import load_dotenv
from utils import convert_geo, write as write_json

load_dotenv(Path(__file__).parents[1] / '.env')
CRS = "EPSG:2154"#lambert
data_path = Path(os.getenv('DATA_PATH'))
filter_pattern = re.compile(r'.*.gpkg')

def get(url, force:bool=True) -> Path:

    zip_file = data_path / 'bd_topo_75.7z'
    # Download if force or not exist
    if force or (not zip_file.exists()):
        req = requests.get(url)
        with zip_file.open('wb') as f:
            f.write(req.content)

    with py7zr.SevenZipFile(str(zip_file), 'r') as archive:
        allfiles = archive.getnames()
        selective_files = [f for f in allfiles if filter_pattern.match(f)]
        for file in selective_files:
            if force or (not (data_path / file).exists()):
                archive.extract(targets=file,path=str(data_path))

    path_gpkg = data_path / selective_files[0]

    return path_gpkg

def prepare(path_gpkg: Path, quartier):
    df = gpd.read_file(path_gpkg, mask=quartier, crs = CRS, layer='troncon_de_route')
    df = df[['nom_1_gauche', 'largeur_de_chaussee', 'sens_de_circulation', 'geometry']]
    coordonnees =[]
    coords = ['x','y']
    points =['p1','p2']
    for i, row in df.iterrows():
        new_line = []
        new_point1= dict(zip(coords, row['geometry'].bounds[2:]))
        new_line.append(new_point1)
        new_point2=dict(zip(coords, row['geometry'].bounds[:2]))
        new_line.append(new_point2)
        coordonnees.append(new_line)
    df['coords'] = coordonnees
    df = pd.DataFrame(df)
    df.drop('geometry', axis='columns', inplace=True)
    return df.to_dict(orient='records')

def write(path_road: Path, data, force=True):
    if force or (not path_road.exists()):
        write_json(path_road, data)
