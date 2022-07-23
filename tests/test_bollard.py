from pathlib import Path

from prepare_data.bollard import get, prepare, write, data_path
from prepare_data.utils import load

url = 'https://opendata.paris.fr/api/records/1.0/search/?dataset={dataset}&q=&{list_facet}&rows={rows}&epsg=2154&geofilter.polygon={polygon}'

_path_json =  data_path / 'bollard.json'

_path_bollards = Path(__file__).parent / 'data/bollards-st-augustin.json'

def test_get(quartier):
    data_json = get(url, quartier, force=True)
    assert data_json['nhits'] >= 400
    assert len(data_json['records']) >= 400

def test_prepare():
    data_json = load(_path_json)
    data_bollard = prepare(data_json)
    _data_bollard = load(_path_bollards)
    assert data_bollard['data'][0].keys() == _data_bollard['data'][0].keys()

def test_write():
    path_bollards = data_path / 'bollard.json'
    _data_bollards = load(_path_bollards)
    write(path_bollards, _data_bollards)
    assert path_bollards.stat().st_size >= 38000
