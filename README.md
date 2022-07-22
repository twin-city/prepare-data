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

# Docker Version

The docker image of this package is built with github action and stored [here](https://github.com/orgs/twin-city/packages/container/package/prepare-data).

- To build it locally :
```
docker build -t prepare_data .
```

- To test is locally :
```
docker run -v $PWD/prepare_data:/prepare_data -v $PWD/tests:/tests -v $PWD/data:/data prepare_data sh -c "pytest tests"
```

# FastAPI

The package *prepare_data* is served by FastAPI, available in the docker image.

- To launch locally :
```
docker run --rm -p 8080:80 -v $PWD/prepare_data:/prepare_data -v $PWD/data:/data --name prepare_data_fastapi prepare_data
```
- To test is locally:
```
curl -X 'GET' 'http://localhost:8080/generate/?x1=649985&y1=6864006&x2=650266&y2=6864226' -H 'accept: application/json'
{"link": "https://.."}
```
