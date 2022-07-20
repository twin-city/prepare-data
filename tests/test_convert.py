from coco_convert import require_dir, get_sub_folders, get_anno_file, open_json, get_perception_categories, get_perception_annotations, convert_perception
from pathlib import Path

path_coco = Path(__file__).parent / 'data/perception'

def test_conversion():
    mainfile = convert_perception(path_coco)
    assert len(mainfile['annotations']) == 23195
    assert mainfile['annotations'][1] == {'id': 1, 'image_id': 0, 'category_id': 1, 'bbox': [309.0, 7.0, 2.0, 1.0], 'area': 2, 'segmentation': None, 'iscrowd': 0}
    assert mainfile['images'][300] == {'id': 300, 'width': 1024, 'height': 768, 'filename': 'RGB282b45af-4c5e-4a0a-8751-a2603bebca6b/rgb_44.png', 'license': None, 'flickr_url': '', 'coco_url': '', 'date_captured': '0:00'}
    