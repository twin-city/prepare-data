from building import get, prepare, write
from pathlib import Path


url = 'https://static.data.gouv.fr/resources/base-de-donnee-nationale-des-batiments-version-0-6/20220427-184828/bnb-export-75.gpkg.zip'

def test_get():
    path_file = get(url, force=False)
    import pdb; pdb.set_trace()

def test_prepare(quartier):
    data_arbres = prepare(get(url), quartier)
    assert len(data_arbres)== 122

def test_write():
    write(prepare(get(url)))
