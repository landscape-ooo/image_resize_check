#!/usr/local/bin/python2.7
# encoding: utf-8
'''
Created on 2015年7月8日

@author: a11
'''
import multiprocessing as mp
import time
import HttpHelper
import queue

log_path = '/tmp/temp.txt'

def worker2(arg,uri, q):
    start = time.clock()
    print start
    client = HttpHelper.HttpHelper()
    t_p = client.processByCurlCallback(uri)
    
    res = 'Process' + str(arg), t_p, done
    q.put(res)

    return res

def listener(q):
    '''listens for messages on the q, writes to file. '''

    f = open(log_path, 'wb') 
    while 1:
        m = q.get()
        print m
        if m == 'kill' or  m=="kill123":
            f.write('killed'+m)
            break
        f.write(str(m) + '\n')
        f.flush()
    f.close()

def main():
    '''
    save access
    '''
    accesslog_path="""/tmp/sohu.log"""
    
    e = queue.loadDataSpring ()
    urlset=e.job_exectt()
    
    f = open(accesslog_path, 'wb') 
    for i in urlset:
        uri="http://image.ganjistatic1.com"+i
        f.write(str(uri) + '\n')
        f.flush()

    f.close()
    
    
    
    # must use Manager queue here, or will not work
    manager = mp.Manager()
    q = manager.Queue()    
    pool = mp.Pool(mp.cpu_count() + 2)

    # put listener to work first
    watcher = pool.apply_async(listener, (q,))

    # fire off workers
    jobs = []
    f = open(accesslog_path, 'rb') 
    
    try:
        for i in range(80):
            sohu_uri=f.readline()
            job = pool.apply_async(worker2, (i,sohu_uri, q))
            jobs.append(job)
    
        # collect results from the workers through the pool result queue
        for job in jobs: 
            job.get()
    except Exception as inst:
        print inst
        q.put('kill123')
        f.close()
        pool.close()
        
    # now we are done, kill the listener
    q.put('kill')
    f.close()
    pool.close()

if __name__ == "__main__":
   main()
