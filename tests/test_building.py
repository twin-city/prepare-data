from building import get, prepare, write
from pathlib import Path

CRS = "EPSG:2154"#lambert
url = 'https://static.data.gouv.fr/resources/base-de-donnee-nationale-des-batiments-version-0-6/20220427-184828/bnb-export-75.gpkg.zip'
quartier = gpd.GeoSeries([Polygon([[(649985, 6864006), (650266, 6864006),(650266, 6864226), (649985, 6864226),  (649985, 6864006)]])])
quartier =  quartier.set_crs(CRS) # lambert

def test_get():
    path_file = get(url)
    import pdb; pdb.set_trace()

def test_save():
    save(get(url), path)

def test_prepare():
    data_arbres = prepare(get(url), quartier)
    assert len(data_arbres)== 122

def test_write():
    write(prepare(get(url)))