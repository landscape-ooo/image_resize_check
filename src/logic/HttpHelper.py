#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2015年7月8日

@author: a11
'''
import urllib2
import urlparse
from PIL import ImageFile
import multiprocessing as mp
import time
from pickle import INST

import queue 

class HttpHelper(object):
    '''
    classdocs
    '''
        
    def  getsizesByCurl(self, uri):
        # get file size *and* image size (None if not known)
        try:
            file = urllib2.urlopen(uri, timeout=5)
            size = file.headers.get("content-length")
            if size: size = int(size)
            p = ImageFile.Parser()
            while 1:
                data = file.read(1024)
                if not data:
                    break
                p.feed(data)
                if p.image:
                    return p.image.size
                    break
            
        except Exception as inst:
            raise  
        finally:
            if file:
                file.close()
                
        return  None    
    
    
    def getSohuuri(self,uri):
        p = urlparse.urlparse(uri)
        sohu_uri = p._replace(netloc=p.netloc.replace(p.hostname, 'scs.ganjistatic1.com')).geturl()
        return sohu_uri


        
    def processByCurlCallback(self, sohu_uri,uri):
        '''
        curl image url ,callback 
        '''
        
        sohu_case_info = self.getsizesByCurl(sohu_uri)

        ganji_case_info = self.getsizesByCurl(uri)
         
        if(sohu_case_info != ganji_case_info):
            return uri, sohu_case_info, ganji_case_info
            
        return True    



