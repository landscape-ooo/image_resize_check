#!/usr/local/bin/python2.7
# encoding: utf-8
'''
Created on 2015年7月12日

@author: a11
'''
import HttpHelper
import queue


if __name__ == '__main__':
    accesslog_path="""/tmp/sohu.log"""
	
    '''    
    e = queue.loadDataSpring ()
    urlset=e.job_exectt()
    
    f = open(accesslog_path, 'ab') 
    for i in urlset:
        uri="http://image.ganjistatic1.com"+i
        f.write(str(uri) + '\n')
        f.flush()

    f.close()
    '''

    client = HttpHelper.HttpHelper()
    f = open(accesslog_path, 'rb') 
    
    
    with open(accesslog_path) as f:
        for ganji_uri in f:
            sohu_uri = client.getNewSohuuri(ganji_uri)
            
            try:
                t_p = client.processByCurlCallback(sohu_uri,ganji_uri)
            except Exception as inst:
                e=   sohu_uri,ganji_uri,inst  
                print e
                print "\n"
                continue
            
            
            if t_p!=True:
                    print t_p
                    print "\n"    
    exit("=======")
    pass
