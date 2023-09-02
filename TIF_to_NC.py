from osgeo import gdal
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib
import netCDF4 as nc
import numpy as np
import os
def tiff2nc(path):
    data = gdal.Open(path)
    im_width = data.RasterXSize  # 获取宽度，数组第二维，左右方向元素长度，代表经度范围
    im_height = data.RasterYSize  # 获取高度，数组第一维，上下方向元素长度，代表纬度范围
    im_bands = data.RasterCount  # 波段数
    im_geotrans = data.GetGeoTransform()  # 获取仿射矩阵，含有 6 个元素的元组
    im_data = data.GetRasterBand(1).ReadAsArray(xoff=0, yoff=0, win_xsize=im_width, win_ysize=im_height)
    # 根据im_proj得到图像的经纬度信息
    im_lon = [im_geotrans[0] + i * im_geotrans[1] for i in range(im_width)]
    im_lat = [im_geotrans[3] + i * im_geotrans[5] for i in range(im_height)]

    im_nc = xr.DataArray(im_data, coords=[im_lat, im_lon], dims=['lat', 'lon'])
    return im_nc
lists="C:\\Users\\css_2022\\Desktop\\MERITDEM\\MERITDEM_curvature.tif"
day_nc=tiff2nc(lists)
#day_nc=day_nc*np.pi/180 #转为弧度制
day_nc.plot()
f_w=nc.Dataset(lists.split(".")[0]+".nc",'w',format='NETCDF4')
f_w.createDimension('lat',10801)
f_w.createDimension('lon',10801)
f_w.createVariable('lat',np.float32,('lat'))
f_w.createVariable('lon',np.float32,('lon'))
print(day_nc.coords)
f_w.variables['lat'][:]=day_nc.coords["lat"]
f_w.variables['lon'][:]=day_nc.coords["lon"]
f_w.createVariable('cur',np.float32, ('lat','lon'),fill_value=-340282346638528859811704183484516925440)
f_w.variables['cur'][:] = day_nc
f_w.close()
