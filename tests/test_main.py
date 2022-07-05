from main import main, data_path, path_lights, path_road, path_building, path_tree

def test_main(quartier):
    # get, prepare, save
    main(quartier)
    # test save jsons
    assert path_lights.stat().st_size == 14317
    assert path_road.stat().st_size == 4671
    assert path_building.stat().st_size == 56754
    assert path_tree.stat().st_size == 13211
