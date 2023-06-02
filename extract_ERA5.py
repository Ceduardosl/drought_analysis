#%%
#Extract multiple ERA5 total evaporation
#negative values indicate evaporation.
#positive values indicate condensation.
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

#%%
for dir_nc in list_nc:

    nc_data = xr.open_dataset(dir_nc)
    nc_data.coords["longitude"] = (nc_data.coords["longitude"] + 180) % 360 - 180

    var = list(nc_data.data_vars)[0]
    start_time, end_time = (nc_data.time[0].values, nc_data.time[-1].values)

    lon, lat = np.meshgrid(nc_data["longitude"], nc_data["latitude"])
    df_point = pd.DataFrame({"lon": lon.flatten(), "lat": lat.flatten()})
    gdf_point = gpd.GeoDataFrame(df_point, geometry = gpd.points_from_xy(df_point["lon"], df_point["lat"], crs="EPSG:4326"))

    basins = glob("Shapes/Basins/*.shp")

    for basin in basins:

        shp_basin = gpd.read_file(basin)

        gdf_result = gpd.sjoin(gdf_point, gpd.GeoDataFrame(geometry = shp_basin.geometry), how = "left")
        gdf_result = gdf_result.loc[~np.isnan(gdf_result["index_right"])]
        ins_point = gdf_result[["lon", "lat"]].values[:]
        ins_df = pd.DataFrame(ins_point, columns = ["lon", "lat"])

        var_ins = []

        for i in range(len(ins_df)):
            var_ins.append(nc_data[var].sel(latitude = ins_df["lat"][i], longitude = ins_df["lon"][i]).values)

        var_df = ins_df[["lon", "lat"]].join(pd.DataFrame(var_ins, columns = nc_data["time"]))
        
    if dir_nc == list_nc[0]:
        merged_df = var_df
    else:
        merged_df = merged_df.merge(var_df, how = "inner", on=("lon", "lat"))
    
    merged_df.to_csv("Dados/Extracted_data/Er_{}.csv".format(
    basin.split("\\")[-1].split(".")[0]),
    sep = ";", index = None, header = True)
# %%
mean_df = merged_df.mean(axis = 0)
mean_df.drop(["lon", "lat"], axis = 0, inplace = True)
mean_df.name = "Er (m)"
mean_df.to_csv("Dados/Extracted_data/Mean_Er_{}.csv".format(
    basin.split("\\")[-1].split(".")[0]),
    sep = ";", index = True, header = True)
# %%
