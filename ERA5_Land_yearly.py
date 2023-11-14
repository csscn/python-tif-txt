import subprocess
import os
from multiprocessing import Process

#systemfunc

#akward para
def akwarad_para():
    filelist=subprocess.getoutput("ls ./ERA5LAND*.nc").split('\n') #ls ./*.hdf;ls ./*.nc
    print(filelist)
    for fil in filelist:
        print("ncl_convert2nc "+fil+"&")


def process_one(fil,i): #最小粒度的任务
    name=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    subprocess.getoutput("cdo yearmean "+fil+" "+name[i]+"_yearly.nc") #ncl_convert2nc;"cdo invertlat  "+fil+" "+fil

 
def py_para():
    count=0
    filelist=subprocess.getoutput("ls ./*.nc").split('\n')#ls ./*.hdf
    i=0
    for fil in filelist:
        p=Process(target=process_one,args=(fil,i))
        i=i+1
        p.start()
        count=count+1
        if count==40:
           p.join()
           count=0
    #print(subprocess.getoutput("ls *.nc"))
    #os.system('cdo mergetime MOD10CM*.nc ./MOD10M_200003_201612.nc')
    p.join()
        #process_one(fil)


py_para()
