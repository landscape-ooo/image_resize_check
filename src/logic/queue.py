#!/usr/local/bin/python2.7
# encoding: utf-8
'''
Created on 2015年7月8日

@author: a11
'''
import pycurl
import json
import StringIO
import re 
try:
    # python 3
    from urllib.parse import urlencode
except ImportError:
    # python 2
    from urllib import urlencode

class loadDataSpring(object):
    def job_exectt(self):
        getdata_http=self.getQueueData();
        e=self.parseAccessByReturnUrl(getdata_http)
        return e
    
    def parseAccessByReturnUrl(self,response_data):
        return_list=[]
        
        res_list = json.loads(response_data)
        
        for item in  res_list['hits']['hits']:
            row= item['_source']['message']
            paseInfo_access=map(''.join, re.findall(r'\"(.*?)\"|\[(.*?)\]|(\S+)', row))
            line= paseInfo_access[5]
            line_info=map("".join,re.findall(r'(\S+)',line))
            if line_info[0]=='GET':
                return_list.append(line_info[1])

        return  return_list   
    def getQueueData(self):
        jsonText = ""
        file = open(  os.path.dirname(os.path.realpath(__file__))+"/jsondec.json")
        for line in file.xreadlines():
            jsonText += line
        postdata = json.loads(jsonText)
        p = []
        p.append(postdata['query'])
        postfields = json.dumps(postdata)
          
        c = pycurl.Curl()
        
        c.setopt(c.URL, 'http://10.1.2.98:9200/logstash-img-2015.07.10/_search')
        fout = StringIO.StringIO()
        c.setopt(pycurl.WRITEFUNCTION, fout.write)

        c.setopt(c.POST, 1)
        c.setopt(c.POSTFIELDS, postfields)
        
        c.perform()
        response_data = fout.getvalue()
        c.close()
        
        return response_data

       
        
'''
if __name__ == '__main__':
    e = loadDataSpring()
    e.job_exectt()
    pass
'''