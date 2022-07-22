from pathlib import Path

from prepare_data.building import get, prepare, write, data_path
from prepare_data.utils import load

url = 'https://static.data.gouv.fr/resources/base-de-donnee-nationale-des-batiments-version-0-6/20220427-184828/bnb-export-75.gpkg.zip'
_path_gpkg =  data_path / 'bnb_export_75.gpkg'
_path_building = Path(__file__).parent / 'data/batiments_place_st_augustin_wall.json'

def test_get():
    path_gpkg = get(url, force=False)
    assert path_gpkg == _path_gpkg
    assert path_gpkg.stat().st_size > 1e6

def test_prepare(quartier):
    data_building = prepare(_path_gpkg, quartier)
    _data_building = load(_path_building)
    assert data_building.keys() == _data_building.keys()


def test_write(quartier):
    path_building = data_path / 'building.json'
    data_building = prepare(_path_gpkg, quartier)
    write(path_building, data_building)
    assert path_building.stat().st_size == 56754
