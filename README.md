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
