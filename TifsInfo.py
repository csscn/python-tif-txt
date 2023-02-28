# coding=utf-8
from osgeo import gdal, ogr, osr
import os
import numpy as np
import math

def raster_metadata(data):

    ds = gdal.Open(data)
    metadata = dict()
    # 也可以是 LongName。GTiff 与 GeoTiff 的区别
    metadata['format'] = ds.GetDriver().ShortName
    # 波段数
    #metadata['band_count'] = ds.RasterCount
    # band 1
    band_count = ds.RasterCount
    #band = ds.GetRasterBand(i)
    metadata['nodata'] = ds.GetRasterBand(1).GetNoDataValue()
    # 统计值
    #band_stat = band.GetStatistics(True, True)
    #metadata['min'] = band_stat[0]
    #metadata['max'] = band_stat[1]
    #metadata['mean'] = band_stat[2]
    #metadata['stddev'] = band_stat[3]
    # 空间参考系统
    srs = osr.SpatialReference(ds.GetProjectionRef())
    metadata['proj4'] = srs.ExportToProj4()
    metadata['wkt'] = srs.ExportToWkt()
    # 地理坐标系
    metadata['geocs'] = srs.GetAttrValue('GEOGCS')
    metadata['uom'] = srs.GetAttrValue('UNIT')
    # 投影坐标系
    metadata['projcs'] = srs.GetAttrValue('PROJCS')  # if projected
    metadata['epsg'] = srs.GetAuthorityCode(None)
    # or
    # metadata['srid'] = srs.GetAttrValue('AUTHORITY', 1)
    # 是否有地图投影（平面坐标）
    metadata['is_projected'] = srs.IsProjected()
    # 仿射变换信息，6参数：
    # upper left x, x(w-e) resolution, x skew, upper left y, y skew, y(s-n) resolution
    ulx, xres, xskew, uly, yskew, yres = ds.GetGeoTransform()
    lrx = ulx + (ds.RasterXSize * xres)  # low right x
    lry = uly + (ds.RasterYSize * yres)  # low right y

    metadata['minx'] = ulx
    maxx = lrx  # ulx + xres * ds.RasterXSize
    metadata['maxx'] = maxx
    miny = lry  # uly + yres * ds.RasterYSize
    metadata['miny'] = miny
    metadata['maxy'] = uly
    # 中心点 centroid
    cx = ulx + xres * (ds.RasterXSize / 2)
    cy = uly + yres * (ds.RasterYSize / 2)
    metadata['center_x'] = cx
    metadata['center_y'] = cy
    metadata['xres'] = xres
    metadata['yres'] = yres
    # geographic width
    metadata['width'] = ds.RasterXSize * xres
    # geographic height，negative，负值
    metadata['height'] = ds.RasterYSize * yres
    # image width
    metadata['size_width'] = ds.RasterXSize
    metadata['size_height'] = ds.RasterYSize
    for i in range(band_count):
        j = i+1
        band = ds.GetRasterBand(j)
        band_num='band'+str(j)
        metadata[band_num] = band.ReadAsArray(0,0,ds.RasterXSize,ds.RasterYSize)
    # minx,miny,maxx,maxy
    metadata['extent'] = [ulx, miny, maxx, uly]
    metadata['centroid'] = [cx, cy]
    ds = None
    return metadata


if __name__ == '__main__':

    outpath = './'
    inpath = '/hard/linwy20/LAI/GBOV/V3.0TifHighRes/TifHighRes/'
    alltif = os.listdir(inpath)

    for i in alltif:
        # if i == 'GBOV_LP03_L08_BART_20140325_20140325_001_UOS_V3.0.TIF':
        if os.path.splitext(i)[1] == '.TIF':
            with open(outpath+os.path.splitext(i)[0]+'.txt', 'w') as f:
                # print(i[19:27])
                meta = raster_metadata(inpath+i)
                s_srs = meta['proj4'][16:18]
                ulx = meta['minx']
                uly = meta['maxy']
                dx = meta['xres']
                dy = meta['yres']
                xres = meta['size_width']
                yres = meta['size_height']
                band1 = meta['band1']
                band2 = meta['band2']
                band3 = meta['band3']
                nodata = meta['nodata']
                # print(meta['proj4'])
                fv  = -999
                scal= 10000
                #item = "%30s\nutm " %(i)
                #f.write(item)
                item2 = "%2d %2d %2d ;year/month/day\n" % (int(i[19:23]), int(i[23:25]), int(i[25:27]))
                # %3d %3d\n%8d %8d\n%2d %2d\n%5d\n"  , , int(ulx), int(uly), int(dx), int(dy), int(scal))
                f.write(item2)
                item3 = "utm %d ;projection name and zone number\n" %(int(s_srs))
                f.write(item3)
                item4 = "%d %d ;samples and lines\n" %(int(xres), int(yres))
                f.write(item4)
                item5 = "%f %f ;up left x and upleft y\n" %(ulx,uly)
                f.write(item5)
                item6 = "%d %d ;delta x and delta y\n" %(int(dx), int(abs(dy)))
                f.write(item6)
                item7 = "%d ; scale factor\n" %(int(scal))
                f.write(item7)

                for m in range(xres):
                    #print(m)
                    #idata = "%f\n" % (band[i])
                    #f.write(idata)
                    #print(i)
                    for n in range(yres):
                        if (band2[m][n]==0.) & (band3[m][n]==0.):
                            idata="%d " % (math.trunc((band1[m][n])*10000))
                            f.write(idata)
                        else:
                            nn="%s " % (fv)
                            f.write(nn)

                    f.write("\n")
