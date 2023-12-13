import glob
import h5py
import numpy as np
import os
import pandas as pd
def read_SML3P(fName):
    with h5py.File(fName, 'r') as f:
        group_am = list(f.keys())[1]
        group_pm = list(f.keys())[2]

        lat_am = list(f[group_am].keys())[13]
        lon_am = list(f[group_am].keys())[15]
        sm_am = list(f[group_am].keys())[26]
        flag_am = list(f[group_am].keys())[18]
        
        #处理纬度
        lat_am = f[group_am][lat_am][:,:]
        lat_am[lat_am==-9999] = np.nan
        lat_am = np.nanmean(lat_am,axis =1)
        lat = np.where((lat_am >= 18) & (lat_am <= 54))[0]
        lat_ = lat_am[lat]
        
        #处理经度
        lon_am = f[group_am][lon_am][:,:]
        lon_am[lon_am==-9999] = np.nan
        lon_am = np.nanmean(lon_am,axis = 0)
        lon = np.where((lon_am >= 73) & (lon_am <= 135))[0]
        lon_ = lon_am[lon]

        #处理土壤湿度(经过质量控制)
        sm_am = f[group_am][sm_am][:,:]
        flag_am = f[group_am][flag_am][:,:]
        sm_am[sm_am==-9999] = np.nan 
        #sm_am[(flag_am>>0)&1==1]=np.nan
        sm_am = sm_am[lat,:]
        sm_up = sm_am[:,lon] 
        
        lat_pm = list(f[group_pm].keys())[14]
        lon_pm = list(f[group_pm].keys())[16]
        flag_pm = list(f[group_pm].keys())[19]
        sm_pm = list(f[group_pm].keys())[28]  
        
        sm_pm = f[group_pm][sm_pm][:,:]
        flag_pm = f[group_pm][flag_pm][:,:]
        sm_pm[sm_pm==-9999] = np.nan 
        #sm_pm[(flag_pm>>0)&1==1]=np.nan
        sm_pm = sm_pm[lat,:]
        sm_down = sm_pm[:,lon] 
        
        sm = np.concatenate((sm_up[:, np.newaxis],sm_down[:, np.newaxis]), axis=1)
        sm = np.nanmean(sm,axis = 1)
    return lat_,lon_,sm_up,sm_down,sm

flist = glob.glob(os.path.join(r'E:\SMAP_L3', '*.h5'))
print(flist[1:367])
sm=[]

for fName in flist[1:367]:
    lat_i,lon_i,sm_up_i,sm_down_i,sm_i = read_SML3P(fName)
    
    sm.append(sm_i)