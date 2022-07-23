from prepare_data.main import main, data_path, path_lights, path_road, path_building, path_tree, path_bollard

def test_main(quartier):
    # get, prepare, save
    main(quartier)
    # test save jsons
    assert path_lights.stat().st_size > 14000
    assert path_road.stat().st_size > 4000
    assert path_building.stat().st_size > 56000
    assert path_tree.stat().st_size > 13000
    assert path_bollard.stat().st_size > 38000
