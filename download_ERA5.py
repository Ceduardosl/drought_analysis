#%%
import cdsapi
#%%
c = cdsapi.Client()
for i in range(1950, 2023+1, 1):
    c.retrieve(
        'reanalysis-era5-land-monthly-means',
        {
            'variable': 'total_evaporation',
            'product_type': 'monthly_averaged_reanalysis',
            'year': str(i),
            'month': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12',
            ],
            'time': '00:00',
            'format': 'netcdf',
        },
        'Dados/ERA5_Data/ERA5_ET_{}.nc'.format(i))
#%%
