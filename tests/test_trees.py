from tree import get, prepare, write, data_path
from pathlib import Path
from utils import load
from fixture import quartier

url ='https://opendata.paris.fr/explore/dataset/les-arbres/download/?format=json&timezone=Europe/Berlin&lang=fr&epsg=2154'
url = 'https://opendata.paris.fr/api/records/1.0/search/?dataset={dataset}&q=&{list_facet}&epsg=2154&geofilter.polygon={polygon}'

_path_json =  data_path / 'les-arbres.json'

_path_tree = Path(__file__).parent / 'data/les-arbres-st-augustin.json'

def test_get():
    data_json = get(url, quartier, True)
    assert data_json['nhits'] == 122
    import pdb; pdb.set_trace()

def test_prepare(quartier):
    data_json = load(_path_json)
    data_tree = prepare(data_json, quartier)
    assert len(data_tree)== 122


#https://opendata.paris.fr/api/records/1.0/search/?dataset=les-arbres&q=&facet=libellefrancais&facet=genre&facet=espece&facet=varieteoucultivar&facet=circonferenceencm&facet=hauteurenmf&epsg=2154&geofilter.polygon=(649985%2C6864006)%2C(650266%2C6864006)%2C(650266%2C6864226)%2C(649985%2C6864226)%2C(649985%2C6864006)
#                                                                                                                                                                                                                (48.883086%2C2.379072)%2C(48.879022%2C2.379930)%2C(48.883651%2C2.386968)
