# encoding: utf-8

import requests
import cStringIO
import Queue
import os
from ds_store import DSStore
import urlparse
from threading import Thread, activeCount
import sys

queue=Queue.Queue()


def fetch_ds_store(ds_store):
    dirs_file = []
    print ds_store
    result=requests.get(ds_store)
    res=result.content
    urlobject = urlparse.urlsplit(ds_store)

    if ds_store.endswith('.DS_Store'):
        base_url = ds_store.rstrip('.DS_Store')
        if result.status_code==200:
            folder_name = urlobject.netloc.replace(':', '_') + '/'.join(urlobject.path.split('/')[:-1])
            if not os.path.exists(folder_name):
                try:
                    os.mkdir(folder_name)
                except:
                    pass
            s = cStringIO.StringIO()
            s.write(res)
            try:
                with DSStore.open(s, 'r') as d:
                    for i in d:
                        if base_url + i.filename not in dirs_file:
                            dirs_file.append(base_url + i.filename)
                            dirs_file.append(base_url + i.filename + '/.DS_Store')
            except:
                print 'open file:'+ds_store+' failed'

            if dirs_file:
                for i in dirs_file:
                    queue.put(i)
    else:
        if result.status_code==403:
            folder_name=urlobject.netloc.replace(':', '_')+'/'+urlobject.path
            if not os.path.exists(folder_name):
                os.mkdir(folder_name)
        else:
            with open(urlobject.netloc.replace(':', '_') + '/'+urlobject.path, 'wb') as file:
                file.write(res)

if __name__ == '__main__':
    if len(sys.argv)==1:
        print '[*]python '+__file__+' URL地址'
        exit()
    fetch_ds_store(sys.argv[1])
    while queue.qsize() > 0:
        if activeCount() <= 5:
            Thread(target=fetch_ds_store, args=(queue.get(),)).start()
