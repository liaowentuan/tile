#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib2
from threading import Thread
import os, sys
import math
from gmap_utils import *

import time

def download_tiles(zoom, lat_start, lat_stop, lon_start, lon_stop, satellite=True):

    start_x, start_y = bd_latlng2xy(zoom, lat_start, lon_start)
    stop_x, stop_y = bd_latlng2xy(zoom, lat_stop, lon_stop)
    
    start_x = int(start_x//256)
    start_y = int(start_y//256)
    stop_x = int(stop_x//256)
    stop_y = int(stop_y//256)
    
    print "x range", start_x, stop_x
    print "y range", start_y, stop_y
    
    for x in xrange(start_x, stop_x):
        # download(x, y, zoom)
        FastThread(x, start_y, stop_y, zoom, satellite).start()


class FastThread(Thread):
    def __init__(self, x, start_y, stop_y, zoom, satellite):
        super(FastThread, self).__init__()
        self.x = x
        self.start_y = start_y
        self.stop_y = stop_y
        self.zoom = zoom
        self.satellite = satellite
    
    def run(self):
        print(xrange(self.start_y, self.stop_y))
        for y in xrange(self.start_y, self.stop_y):
            print("True",self.start_y,self.stop_y)
            if satellite:
                download_satellite(self.x, y, self.zoom)
                download_tile(self.x, y, self.zoom, True)
            else:
                download_tile(self.x, y, self.zoom)


def download_tile(x, y, zoom, satellite=False):
    url = None
    filename = None
    dirPath = "%s/%s" % ( zoom, x)
    mkdir(dirPath)
    folder = "road/" if satellite else "%s/%s/" % (zoom, x)
    scaler = "" if satellite else "&scaler=1"
    # styles is roadmap when downloading satellite
    styles = "sl" if satellite else "pl"

    query = "qt=tile&x=%d&y=%d&z=%d&styles=%s%s&udt=20180131.png" % (x, y, zoom, styles, scaler)
    url = "http://online2.map.bdimg.com/tile/?%s"%(query) 
    filename = "%s.png"%(y)

    download_file(url, filename, folder)

'''
def download_satellite(x, y, zoom):
    url = None
    filename = None
    folder = "it/"

    path = "u=x=%d;y=%d;z=%d;v=009;type=sate&fm=46&udt=20170927" % (x, y, zoom)
    url = "http://shangetu0.map.bdimg.com/it/" + path
    filename = path.replace(";", ",") + ".jpg"

    download_file(url, filename, folder)
'''

def download_file(url, filename, folder=""):
    full_file_path = folder + filename
    if not os.path.exists(full_file_path):
        bytes = None
        try:
            req = urllib2.Request(url, data=None)
            response = urllib2.urlopen(req)
            bytes = response.read()
        except Exception, e:
            print "--", filename, "->", e
            sys.exit(1)
        
        if bytes.startswith("<html>"):
            print "-- forbidden", filename
            sys.exit(1)
        
        print "-- saving " + filename
        
        f = open(full_file_path, 'wb')
        f.write(bytes)
        f.close()
        
        time.sleep(5) # 调整速率
    else:
        print "-- existed " + filename
            
def mkdir(path):
    # 判断结果
    path=path.strip() # window 调用
    isExists=os.path.exists(path)
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path) 
        return True

if __name__ == "__main__":
    arr = [9,8,7,6,5,4,3,2]
    for i in arr:    
        zoom = i

        lat_start,lon_start = -74,0  # world
        lat_stop,lon_stop = 80,360  # world
        if i > 9:
            lat_start,lon_start = -12,60  # china
            lat_stop,lon_stop = 56,150  # china

        satellite = False
	
        download_tiles(zoom, lat_start, lat_stop, lon_start, lon_stop, satellite)
