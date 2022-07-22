from tree import get, prepare, write, data_path
from pathlib import Path
from utils import load

url = 'https://opendata.paris.fr/api/records/1.0/search/?dataset={dataset}&q=&{list_facet}&rows={rows}&epsg=2154&geofilter.polygon={polygon}'

_path_json =  data_path / 'les-arbres.json'

_path_tree = Path(__file__).parent / 'data/les-arbres-st-augustin.json'

def test_get(quartier):
    data_json = get(url, quartier, force=True)
    assert data_json['nhits'] > 100
    assert len(data_json['records']) > 100

def test_prepare():
    data_json = load(_path_json)
    data_tree = prepare(data_json)
    _data_tree = load(_path_tree)
    assert data_tree['data'][0].keys() == _data_tree['data'][0].keys()

def test_write():
    path_tree = data_path / 'tree.json'
    _data_tree = load(_path_tree)
    write(path_tree, _data_tree)
    assert path_tree.stat().st_size == 13221
