import argparse
import building
import tree
import utils
import road
import light
import os
from pathlib import Path

light_url = 'https://opendata.paris.fr/api/records/1.0/search/?dataset={dataset}&q=&{list_facet}&rows={rows}&epsg=2154&geofilter.polygon={polygon}'
data_path = Path(os.getenv('DATA_PATH'))
path_lights = data_path / 'light.json'

def main(neighborhood):
    data_light=light.prepare(light.get(light_url, neighborhood, force = True))
    import pdb; pdb.set_trace()
    light.write(path_lights, data_light)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("x1", type=float, help="Bottom left x coordinate")
    parser.add_argument("y1", type=float, help="Bottom left y coordinate")
    parser.add_argument("x2", type=int, help="Top right x coordinate")
    parser.add_argument("y2", type=int, help="Top right y coordinate")
    args = parser.parse_args()

    #print(f"{args.x1},{args.y1},{args.x2},{args.y2} ")
    main(args.x1, args.y1, args.x2, args.y2)


"""def coords2d(s):
    try:
        x, y = map(int, s.split(','))
        return x, y
    except:
        raise argparse.ArgumentTypeError("Coordinates must be x,y")

parser.add_argument('--cord', help="Coordinate", dest="cord", type=coords2d, nargs=2)
args = parser.parse_args()
print(f"{args.cord}")"""