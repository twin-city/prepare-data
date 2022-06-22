from pathlib import Path
from typing import List
import json

def write(path: Path, obj):
    # write JSON files:
    with path.open("w", encoding="UTF-8") as target:
        json.dump(obj, target)


def load(path: Path):
    # read JSON files:
    with path.open(encoding="UTF-8") as source:
         obj = json.load(source)
    return obj

def convert_geo(list_geo: list, type_geo:str) -> List[dict]:
    """Convert list of points to list of dict of points"""
    dict_geo = {"type": type_geo, "coordonnees": []}
    for point in list_geo:
        dict_geo['coordonnees'] += [{'x':point[0], "y":point[1]}]
    return dict_geo

def create_geoseries(x1, x2, y1, y2):
    #create neighborhood polygon
    quartier = gpd.GeoSeries([Polygon([[(x1,y1), (x2,y1), (x2, y2),(x1,y2), (x1,y1)]])])
    quartier = quartier.set_crs(CRS)
    return quartier
