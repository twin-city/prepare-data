from road import get, write, prepare, data_path
from pathlib import Path
import geopandas as gpd
from geojson import Polygon
from utils import load

url = 'https://wxs.ign.fr/859x8t863h6a09o9o6fy4v60/telechargement/prepackage/BDTOPOV3-TOUSTHEMES-DEPARTEMENT_GPKG_PACK_221$BDTOPO_3-0_TOUSTHEMES_GPKG_LAMB93_D075_2022-03-15/file/BDTOPO_3-0_TOUSTHEMES_GPKG_LAMB93_D075_2022-03-15.7z'
_path_gpkg =  data_path / 'BDTOPO_3-0_TOUSTHEMES_GPKG_LAMB93_D075_2022-03-15/BDTOPO/1_DONNEES_LIVRAISON_2022-03-00088/BDT_3-0_GPKG_LAMB93_D075-ED2022-03-15/BDT_3-0_GPKG_LAMB93_D075-ED2022-03-15.gpkg'
_path_road = Path(__file__).parent / 'data/les-routes-st-augustin.json'

def test_get():
    path_gpkg = get(url, force=False)
    assert path_gpkg == _path_gpkg
    assert path_gpkg.stat().st_size > 1e6

def test_prepare(quartier):
    data_road = prepare(_path_gpkg, quartier)
    _data_road = load(_path_road)
    assert data_road == _data_road

def test_write(quartier):
    path_road = data_path / 'road.json'
    data_road = prepare(_path_gpkg, quartier)
    write(path_road, data_road)
    assert path_road.stat().st_size >= 4000
