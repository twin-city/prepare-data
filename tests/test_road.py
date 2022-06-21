from road import get, write, prepare
from pathlib import Path
import geopandas as gpd
from geojson import Polygon

url = 'https://wxs.ign.fr/859x8t863h6a09o9o6fy4v60/telechargement/prepackage/BDTOPOV3-TOUSTHEMES-DEPARTEMENT_GPKG_PACK_221$BDTOPO_3-0_TOUSTHEMES_GPKG_LAMB93_D075_2022-03-15/file/BDTOPO_3-0_TOUSTHEMES_GPKG_LAMB93_D075_2022-03-15.7z'
CRS = "EPSG:2154"#lambert
quartier_st_aug =gpd.GeoSeries([Polygon([[(649985, 6864006), (650266, 6864006),(650266, 6864226), (649985, 6864226),  (649985, 6864006)]])])
quartier_st_aug =  quartier_st_aug.set_crs(CRS)
data_path = Path('/workspace/home/data')

def test_get():
    get_path = get(url, data_path)
    assert get_path==Path('/workspace/home/data')

def test_prepare():
    data_road = prepare(quartier_st_aug, data_path)
    assert 'coordonnees' in data_road.columns