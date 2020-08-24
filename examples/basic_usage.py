from usgspy import usgs
from usgspy.mapping import has_gpd,pd_to_gpd

import matplotlib.pyplot as plt 

eqs = usgs.earthquakes(debug_level = 1, use_gpd = False, init_calls = False)


query_dict = dict(
    minlatitude=10.,
    minlongitude=-180,
    maxlatitude=80,
    maxlongitude=-100,
    minmagnitude=3.5,
)

cc = eqs.count(**query_dict)
print(f"this query has {cc} records")

query_dict['format'] = 'csv'
df = eqs.query(**query_dict)

print(df.head())

df.plot.scatter('longitude','latitude',c='depth')
plt.show()

if has_gpd:
    import geopandas as gpd 
    df_gpd = pd_to_gpd(df,'latitude','longitude')

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    ax = world[world.continent == 'North America'].plot(color='white', edgecolor='black')
    df_gpd.plot(ax=ax, c=df['depth'])

    plt.show()
