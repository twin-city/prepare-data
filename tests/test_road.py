from road import get, create_quartier, write, prepare
from pathlib import Path
import geopandas as gpd
from geojson import Polygon

url = 'https://wxs.ign.fr/859x8t863h6a09o9o6fy4v60/telechargement/prepackage/BDTOPOV3-TOUSTHEMES-DEPARTEMENT_GPKG_PACK_221$BDTOPO_3-0_TOUSTHEMES_GPKG_LAMB93_D075_2022-03-15/file/BDTOPO_3-0_TOUSTHEMES_GPKG_LAMB93_D075_2022-03-15.7z'
CRS = "EPSG:2154"#lambert
quartier_st_aug =gpd.GeoSeries([Polygon([[(649985, 6864006), (650266, 6864006),(650266, 6864226), (649985, 6864226),  (649985, 6864006)]])])
quartier_st_aug =  quartier_st_aug.set_crs(CRS)

def test_create():
    quartier = create_quartier(649985, 650266, 6864006, 6864226)
    assert quartier == quartier_st_aug



def test_get():
    quartier = create_quartier(649985, 650266, 6864006, 6864226)
    data = get(url, quartier)
    assert len(data)==26

def test_prepare():
    quartier = create_quartier(649985, 650266, 6864006, 6864226)
    data = get(url, quartier)
    data_road = prepare(data)
    assert data_road.contains('coordonnees')