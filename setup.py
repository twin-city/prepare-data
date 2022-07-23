from setuptools import setup, find_packages

setup(name="prepare_data",
      packages=find_packages(),
      install_requires = [
            'pandas>=1.2.0',
            'geopandas>=0.10.2',
            'wget==3.2',
            'requests==2.27.1',
            'zipfile38==0.0.3',
            'geojson==2.5.0',
            'pyproj==3.3.1',
            'py7zr==0.18.9',
            'python-dotenv==0.20.0',
      ]
     )
