from light import get, prepare, write, data_path
from pathlib import Path
from utils import load

url = 'https://opendata.paris.fr/api/records/1.0/search/?dataset={dataset}&q=&{list_facet}&rows={rows}&epsg=2154&geofilter.polygon={polygon}'

_path_json =  data_path / 'light.json'

_path_lights = Path(__file__).parent / 'data/lights-st-augustin.json'

def test_get(quartier):
    data_json = get(url, quartier, force=True)
    assert data_json['nhits'] == 124
    assert len(data_json['records']) == 124

def test_prepare():
    data_json = load(_path_json)
    data_lights = prepare(data_json)
    _data_lights = load(_path_lights)
    assert data_lights == _data_lights

def test_write():
    path_lights = data_path / 'light.json'
    _data_lights = load(_path_lights)
    write(path_lights, _data_lights)
    assert path_lights.stat().st_size == 14317
