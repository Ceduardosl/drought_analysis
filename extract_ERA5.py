#%%
#Extract multiple CRU data from multiple shapefiles
__author__ = "Carlos Eduardo Sousa Lima"
__license__ = "GPL"
__version__ = "2.0"
__email__ = "ce-lima@hotmail.com"
__maintainer__ = "Carlos Eduardo Sousa Lima"
__status__ = "Production"

import pandas as pd
import geopandas as gpd
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from glob import glob

list_nc = glob("Dados/ERA5_data/*.nc")


dir_nc = list_nc[0]

nc_data = xr.open_dataset(dir_nc)

var = list(nc_data.data_vars)[0]
#%%
lon, lat = np.meshgrid(nc_data["lon"], nc_data["lat"])
df_point = pd.DataFrame({"lon": lon.flatten(), "lat": lat.flatten()})
shp_point = gpd.GeoDataFrame(df_point, geometry = gpd.points_from_xy(df_point["lon"], df_point["lat"], crs="EPSG:4326"))

basins = glob("Shapes/Basins/*.shp")

for basin in basins:
    shp_basin = gpd.read_file(basin)

    gdf_result = gpd.sjoin(shp_point, gpd.GeoDataFrame(geometry = shp_basin.envelope), how = "left")
    gdf_result = gdf_result.loc[~np.isnan(gdf_result["index_right"])]
    ins_point = gdf_result[["lon", "lat"]].values[:]
    ins_df = pd.DataFrame(ins_point, columns = ["lon", "lat"])

    var_ins = []

    for i in range(len(ins_df)):
        var_ins.append(nc_data[var].sel(lat = ins_df["lat"][i], lon = ins_df["lon"][i]).values)

    var_df = ins_df[["lon", "lat"]].join(pd.DataFrame(var_ins, columns = nc_data["time"]))
    var_df.to_csv("Dados/Extracted_data/{}_{}_{}_{}.csv".format(
        basin.split("\\")[-1].split(".")[0],
        var,
        nc_data.time_coverage_start,
        nc_data.time_coverage_end), sep = ";", index = None, header = True)