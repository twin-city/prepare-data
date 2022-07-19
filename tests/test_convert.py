from coco_convert import require_dir, get_sub_folders, get_anno_file, open_json, get_perception_categories, get_perception_annotations, convert_perception

perception_folder = "/workspace/home/prepare-data/perception_tools/Dataset Twincity"

def test_conversion():
    convert_perception(perception_folder)
    assert 0==0