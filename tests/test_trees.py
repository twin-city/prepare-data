from tree import get, prepare, save, write
from pathlib import Path

url ='https://opendata.paris.fr/explore/dataset/les-arbres/download/?format=json&timezone=Europe/Berlin&lang=fr&epsg=2154'
path = '/workspace/home/data/arbres_paris.json'
 
def test_get():
    data_tree = get(url)
    assert type(data_tree) == list

def test_save():
    save(get(url), path)

def test_prepare():
    data_arbres = prepare(get(url))
    assert len(data_arbres)== 122

def test_write():
    write(prepare(get(url)))