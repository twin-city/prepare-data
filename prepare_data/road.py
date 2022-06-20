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

CRS = "EPSG:2154"#lambert
data_path = Path('/workspace/home/data')
filter_pattern = re.compile(r'.*.gpkg')

def get(url):
    req = requests.get(url)
    file_name = 'bd_topo_75.7z'
    with (data_path / file_name).open('wb') as f:
        f.write(req.content)
    with py7zr.SevenZipFile(str(data_path /'bd_topo_75.7z'), 'r') as archive:
        allfiles = archive.getnames()
        selective_files = [f for f in allfiles if filter_pattern.match(f)]
        print(selective_files)
        archive.extract(targets=selective_files,path=str(data_path))