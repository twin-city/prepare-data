import os
import pandas as pd
import geopandas as gpd
import json
from pathlib import Path
import zipfile
import re
import requests
from dotenv import load_dotenv
from utils import convert_geo, write as write_json
from math import nan
from shapely.geometry import Polygon, LineString, MultiLineString, MultiPolygon, collection

load_dotenv(Path(__file__).parents[1] / '.env')
CRS = "EPSG:2154"#lambert
data_path = Path(os.getenv('DATA_PATH'))
filter_pattern = re.compile(r'(.*).gpkg$')

def get(url, force: bool=False) -> Path:
    """Télécharge et retourne le fichier gpkg"""

    zip_file = data_path / 'bdnb_75.zip'
    # Download if fore or not exist
    if force or (not zip_file.exists()):
        req = requests.get(url)
        with zip_file.open('wb') as f:
            f.write(req.content)

    with zipfile.ZipFile(str(zip_file), 'r') as archive:
        allfiles = archive.namelist()
        selective_files = [f for f in allfiles if filter_pattern.match(f)]
        for file in selective_files:
            if force or (not (data_path / file).exists()):
                archive.extract(file, path=data_path)

    path_gpkg = data_path / selective_files[0]
    return path_gpkg

def prepare(path_gpkg:Path, quartier):
    """Lit le gpkg et filtre les données de quartier"""
    df_source = gpd.read_file(path_gpkg, mask=quartier, crs = CRS)
    df_source = df_source[['bnb_id', 'cerffo2020_annee_construction', 'cerffo2020_mat_mur_txt', 'cerffo2020_mat_toit_txt', 'igntop202103_bat_hauteur', 'geometry']]
    df_explode = df_source.explode(ignore_index=True)

    list_batiments = []
    list_artifacts = []
    list_wall = []

    col_to_save = {"bnb_id":"id",
                   "cerffo2020_annee_construction": "annee_construction",
                  "cerffo2020_mat_mur_txt": "mat_mur",
                  "cerffo2020_mat_toit_txt": "mat_toit",
                  "igntop202103_bat_hauteur": "hauteur",
                  }

    df_explode = df_explode.replace({nan: None})

    for i, row1 in df_explode.iterrows():
        print(f'-----{row1.bnb_id}-----')
        list_coords = []
        list_coords_int = []
        list_coords_ext = [[x,y] for x,y in zip(*row1['geometry'].exterior.coords.xy)]
        list_coords_int_xy = [ring.coords.xy for ring in row1['geometry'].interiors]
        for coords_int_xy in list_coords_int_xy:
            coords_int = [[x,y] for x,y in zip(*coords_int_xy)]
            if len(coords_int) == 2:
                continue
            if len(list_coords_int) > 0:
                #import pdb; pdb.set_trace()
                last_point = list_coords_int[-1]
                first_point = coords_int[0]
                list_artifacts += [[last_point, first_point]]
                #list_coords_int[-1] += [last_point]

            list_coords_int += coords_int

        if len(list_coords_int) > 0:
            last_point = list_coords_ext[-1]
            first_point = list_coords_int[0]
            list_coords = list_coords_ext + list_coords_int# + [last_point]
            list_artifacts += [[last_point, first_point]]
        else:
            list_coords = list_coords_ext
        # rename row index and drop useless
        ro_to_save = row1.rename(col_to_save)[col_to_save.values()].to_dict()

        ro_to_save.update(convert_geo(list_coords, type_geo='polygone'))
        list_batiments += [ro_to_save]

        for j, row2 in df_explode.iterrows():
            if i > j :
                intersection = row1['geometry'].intersection(row2['geometry'])
                if intersection.is_empty:
                    continue
                if type(intersection) is LineString :
                    list_wall.append([[x,y] for x,y in zip(*intersection.xy)])
                elif type(intersection) is MultiLineString :
                    for wall in list(intersection):
                        list_wall.append([[x,y] for x,y in zip(*wall.xy)])

    dict2save = dict(
        buildings=list_batiments,
        artifacts=[convert_geo(artifacts, 'segment') for artifacts in list_artifacts],
        walls=[convert_geo(wall, 'segment') for wall in list_wall])

    return dict2save

def write(path_building: Path, data, force=True):
    if force or (not path_building.exists()):
        write_json(path_building, data)
