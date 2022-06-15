import pytest
import geopandas as gpd
from geojson import Polygon

CRS = "EPSG:2154"#lambert
saint_augustin = [[(649985, 6864006), (650266, 6864006),(650266, 6864226), (649985, 6864226),  (649985, 6864006)]]

@pytest.fixture
def quartier():
    quartier=gpd.GeoSeries([Polygon(saint_augustin)])
    quartier =  quartier.set_crs(CRS) # lambert
    return quartier
