import pytest
from utils import convert2poly

x1, y1, x2, y2 = 649985, 6864006, 650266, 6864226

@pytest.fixture
def quartier():
    #quartier = gpd.GeoSeries([Polygon(saint_augustin)])
    #quartier =  quartier.set_crs(CRS) # lambert
    return convert2poly(x1, y1, x2, y2)
