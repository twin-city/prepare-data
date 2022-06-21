import os
import pandas as pd
import geopandas as gpd
import geojson
import json
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import shapely
from shapely.geometry import Polygon, LineString, MultiLineString, MultiPolygon, collection
from pathlib import Path
import requests
from geojson import Polygon
import py7zr
import re

CRS = "EPSG:2154"#lambert
data_path = Path('/workspace/home/data')
filter_pattern = re.compile(r'.*.gpkg')

def create_quartier(x1, x2, y1, y2):
    quartier = gpd.GeoSeries([Polygon([[(x1,y1), (x2,y1), (x2, y2),(x1,y2), (x1,y1)]])])
    quartier = quartier.set_crs(CRS)
    return quartier

def get(url, quartier):
    req = requests.get(url)
    file_name = 'bd_topo_75.7z'
    with (data_path / file_name).open('wb') as f:
        f.write(req.content)
    with py7zr.SevenZipFile(str(data_path /'bd_topo_75.7z'), 'r') as archive:
        allfiles = archive.getnames()
        selective_files = [f for f in allfiles if filter_pattern.match(f)]
        print(selective_files)
        archive.extract(targets=selective_files,path=str(data_path))
    df = gpd.read_file(data_path / selective_files[0], mask=quartier, crs = CRS, layer='troncon_de_route')
    import pdb; pdb.set_trace()
    return df

def prepare(df):
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
    df['coordonnees'] = coordonnees
    df.drop('geometry', axis='columns', inplace=True)
    import pdb; pdb.set_trace()
    return df

def write(path_quartier: Path, data):
    data.to_json(path_quartier, orient = "table")