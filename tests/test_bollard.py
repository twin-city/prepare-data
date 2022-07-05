from bollard import get, prepare, write, data_path
from pathlib import Path
from utils import load

url = 'https://opendata.paris.fr/api/records/1.0/search/?dataset={dataset}&q=&{list_facet}&rows={rows}&epsg=2154&geofilter.polygon={polygon}'

_path_json =  data_path / 'bollard.json'

_path_bollards = Path(__file__).parent / 'data/bollards-st-augustin.json'

def test_get(quartier):
    data_json = get(url, quartier, force=True)
    assert data_json['nhits'] == 124
    assert len(data_json['records']) == 124

def test_prepare():
    data_json = load(_path_json)
    data_bollards = prepare(data_json)
    _data_bollards = load(_path_bollards)
    assert data_bollards == _data_bollards

def test_write():
    path_bolards = data_path / 'bollard.json'
    _data_bollards = load(_path_bollards)
    write(path_bollards, _data_bollards)
    assert path_bollards.stat().st_size == 14317
