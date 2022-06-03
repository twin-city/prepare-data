from prepare_data.tree import get, prepare, save

def test_get():
    url = ""
    #import pdb; pdb.set_trace()
    data_tree = get(url)
    assert data_tree == ''
