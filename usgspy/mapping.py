import pandas 
try:
    import geopandas as gpd 
    has_gpd = True
except:
    has_gpd = False

def pd_to_gpd(df,clat='latitude',clon='longitude'):
    df = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df[clon], df[clat])
    )
    return df 
