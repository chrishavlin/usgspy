# usgspy 

A simple python wrapper of the usgs earthquake catologue API https://earthquake.usgs.gov/fdsnws/event/1/

## installation 

download and unpack and then run 

```
pip install .
```

for a bare bones installation. 

To use extra geopandas features, you can run 

```
pip install .[geopandas]
```

If geopandas is available, routines that return pandas dataframes will instead return geodataframes.
