import xarray as xr
import numpy as np
import datetime
import dask
import pandas as pd
import glob, os, shutil, sys
from dask.diagnostics import ProgressBar
from joblib import Parallel, delayed
import subprocess
import pytz
from sklearn.model_selection import train_test_split
from tqdm import tqdm, trange

def get_forcing(Syear, Eyear, mlat, mlon, pathout, site_name):
    path = '/tera07/zhwei/For_QingChen/DataML/forecast/input/forcing/1D_0p1/'
    models = ['tp', 'Q', 'sp', 'ssrd', 'strd', 't2m', 'u10', 'v10', 'swvl1', 'swvl2']

    def forcing(model):
        m = []
        for year in np.arange(Syear, Eyear + 1):
            f = xr.open_dataset(f'{path}ERA5Land_{year}_{model}_1D_0p1.nc', drop_variables='time_bnds')
            ds = f.sel(latitude=mlat, longitude=mlon, method="nearest")
            if np.count_nonzero(~np.isnan(ds[f'{model}'].values)) == 0:
                f1 = f.sel(latitude=mlat, method="nearest")
                f1 = f1.where(f1 > -99, drop=True)
                ds = f1.sel(longitude=mlon, method="nearest")
            m.append(ds[f'{model}'].values)
        m = np.array(np.concatenate(m, axis=0))
        return m

    position = np.array(Parallel(n_jobs=10)(delayed(forcing)(model) for model in models))
    FLUXNET = xr.Dataset(coords={'time': pd.date_range(f'{Syear}-01-01', f'{Eyear}-12-31', freq='1D')})
    for i, model in enumerate(models):
        FLUXNET[f"{model}"] = (("time"), position[i])
    FLUXNET.to_netcdf(pathout + f"{site_name}_Amazon_{Syear}_{Eyear}.nc")



    if __name__ == '__main__':
    path = '/tera07/zhwei/For_QingChen/DataML/FLUXNET/'
    site_data_path = '/tera07/zhwei/For_QingChen/DataML/FLUXNET/input/sitedata/'
    data_save_path = '/tera07/zhwei/For_QingChen/DataML/FLUXNET/input/case6/input/'
    pathout = '/tera07/zhwei/For_QingChen/DataML/FLUXNET/input/case6/model/'
    stnlist = f"{path}/case6_model1.xlsx"
    station_list = pd.read_excel(stnlist, header=0, sheet_name='train_test')  # ,header=0

    for i in range(len(station_list['Site ID'])):
        print(f"processing site: {station_list['Site ID'][i]}, from {station_list['Syear'][i]} to {station_list['Eyear'][i]}")
        if os.path.exists(f'{data_save_path}' + f"{station_list['Site ID'][i]}_forcing.nc"):
            print(station_list['Site ID'][i], ' Done')
        else:
            Syear, Eyear = station_list['Syear'][i], station_list['Eyear'][i]
            mlat, mlon = station_list['lat'][i], station_list['lon'][i]

            get_forcing(Syear, Eyear, mlat, mlon, data_save_path, station_list['Site ID'][i])
