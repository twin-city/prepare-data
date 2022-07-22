from pathlib import Path

from prepare_data.light import get, prepare, write, data_path
from prepare_data.utils import load


url = 'https://opendata.paris.fr/api/records/1.0/search/?dataset={dataset}&q=&{list_facet}&rows={rows}&epsg=2154&geofilter.polygon={polygon}'

_path_json =  data_path / 'eclairage-public.json'

_path_lights = Path(__file__).parent / 'data/lights-st-augustin.json'

def test_get(quartier):
    data_json = get(url, quartier, force=True)
    assert data_json['nhits'] == 124
    assert len(data_json['records']) == 124

def test_prepare():
    data_json = load(_path_json)
    data_lights = prepare(data_json)
    _data_lights = load(_path_lights)
    assert data_lights['data'][0].keys() == _data_lights['data'][0].keys()

def test_write():
    path_lights = data_path / 'light.json'
    _data_lights = load(_path_lights)
    write(path_lights, _data_lights)
    assert path_lights.stat().st_size >= 14000
