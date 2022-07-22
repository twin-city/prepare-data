import argparse
import os, sys
from pathlib import Path
from shapely.geometry import Polygon
from pyproj import Proj, transform

print(Path(__file__).parent.resolve())
sys.path.append(Path(__file__).parent.resolve())

from .light import get as get_light, prepare as prepare_light, write as write_light
from .tree import get as get_tree, prepare as prepare_tree, write as write_tree
from .road import get as get_road, prepare as prepare_road, write as write_road
from .building import get as get_building, prepare as prepare_building, write as write_building
from .bollard import get as get_bollard, prepare as prepare_bollard, write as write_bollard
from .utils import convert2poly


light_url = 'https://opendata.paris.fr/api/records/1.0/search/?dataset={dataset}&q=&{list_facet}&rows={rows}&epsg=2154&geofilter.polygon={polygon}'
road_url = 'https://wxs.ign.fr/859x8t863h6a09o9o6fy4v60/telechargement/prepackage/BDTOPOV3-TOUSTHEMES-DEPARTEMENT_GPKG_PACK_221$BDTOPO_3-0_TOUSTHEMES_GPKG_LAMB93_D075_2022-03-15/file/BDTOPO_3-0_TOUSTHEMES_GPKG_LAMB93_D075_2022-03-15.7z'
building_url = 'https://static.data.gouv.fr/resources/base-de-donnee-nationale-des-batiments-version-0-6/20220427-184828/bnb-export-75.gpkg.zip'
tree_url = 'https://opendata.paris.fr/api/records/1.0/search/?dataset={dataset}&q=&{list_facet}&rows={rows}&epsg=2154&geofilter.polygon={polygon}'
bollard_url = 'https://opendata.paris.fr/api/records/1.0/search/?dataset={dataset}&q=&{list_facet}&rows={rows}&epsg=2154&geofilter.polygon={polygon}'

data_path = Path(os.getenv('DATA_PATH'))

data_path.mkdir(parents=True, exist_ok=True)

path_lights = data_path / 'light.json'
path_road = data_path / 'road.json'
path_building = data_path / 'building.json'
path_tree = data_path / 'tree.json'
path_bollard = data_path / 'bollard.json'

def main(neighborhood):
    data_light = prepare_light(
        get_light(light_url, neighborhood, force = True))
    write_light(path_lights, data_light)

    data_road = prepare_road(
        get_road(road_url, force = False),neighborhood )
    write_road(path_road, data_road)

    data_building = prepare_building(
        get_building(building_url, force = False), neighborhood)
    write_building(path_building, data_building)

    data_tree = prepare_tree(
        get_tree(tree_url, neighborhood, force = True))
    write_tree(path_tree, data_tree)

    data_bollard = prepare_bollard(
        get_bollard(bollard_url, neighborhood, force = True))
    write_bollard(path_bollard, data_bollard)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("x1", type=float, help="Bottom left x coordinate")
    parser.add_argument("y1", type=float, help="Bottom left y coordinate")
    parser.add_argument("x2", type=float, help="Top right x coordinate")
    parser.add_argument("y2", type=float, help="Top right y coordinate")
    parser.add_argument('--CRS', type=str, help='coordinate system  (CRS) of the given coordinates',
        default='EPSG:4326', dest='crs')
    args = parser.parse_args()

    # Convert to LAMBERT if needed
    if args.crs != "EPSG:2154":
        inProj  = Proj('+init='+args.crs, preserve_units=True)
        outProj = Proj("+init=EPSG:2154") #  LAMBERT
        x1, y1 = transform(inProj, outProj, args.y1, args.x1)
        x2, y2 = transform(inProj, outProj, args.y2, args.x2)
    else:
        x1, y1, x2, y2 = args.x1, args.y1, args.x2, args.y2
    print(x1, y1, x2, y2)
    # Convert to shapely polygon
    polygon = convert2poly(x1, y1, x2, y2)
    main(polygon)


"""def coords2d(s):
    try:
        x, y = map(int, s.split(','))
        return x, y
    except:
        raise argparse.ArgumentTypeError("Coordinates must be x,y")

parser.add_argument('--cord', help="Coordinate", dest="cord", type=coords2d, nargs=2)
args = parser.parse_args()
print(f"{args.cord}")"""
