from tree import get, prepare, write, data_path
from pathlib import Path
from utils import load
from fixture import quartier

url ='https://opendata.paris.fr/explore/dataset/les-arbres/download/?format=json&timezone=Europe/Berlin&lang=fr&epsg=2154'
_path_json =  data_path / 'les-arbres.json'

_path_tree = Path(__file__).parent / 'data/les-arbres-st-augustin.json'

def test_get():
    path_json = get(url, True)
    import pdb; pdb.set_trace()
    assert path_json.stat().st_size > 1e7

def test_prepare(quartier):
    data_tree = prepare(_path_json, quartier)
    assert len(data_tree)== 122
