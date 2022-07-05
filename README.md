# Prepare data from open source for the Unity projet

# Create venv

```
python3 -m venv venv
venv/bin/pip3 install -r requirements.txt
source venv/bin/activate
```

# Populate .env

```
mv .env.sample .env
mkdir data
```

-> Change DATA_PATH if needed

# Create all jsons in command line

x1, y1, x2, y2 are WGS84 coordinates or other CRS. Default is WGS84 (EPSG:4326)
```
python prepare_data/main.py x1 y1 x2 y2 --CRS EPSG:2154
```
example on St-Augustin (Paris), coordinate in lambert 93 (EPSG:2154)
```
python prepare_data/main.py 649985 6864006 650266 6864226 --CRS EPSG:2154
```

# TODO

- Build and distribute the package
