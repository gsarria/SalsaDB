#!/usr/bin/python

import os
import glob
import sys
import md5
from multiprocessing import Pool
import taglib
import choruExtractor

def procesar(filename):
    fname = filename.split('/')[-1]
    # foutname = "%s/%s.mp3" % (pathdest,md5.md5(fname).hexdigest())
    # print "%s -> %s.mp3" % (fname,foutname)
    # fin = open(filename,"r")
    # fout = open(foutname,"w")
    # fout.write(fin.read())
    # fin.close()
    # fout.close()
    print filename
    choruExtractor.process(filename,pathdest,fname)
    # s=md5.md5(filename).hexdigest()+".mp3"
    ss=md5.md5(filename).hexdigest()+".wav"
    # dirr=pathdest+fname
    # os.rename(s,fname)
    os.remove(ss)


# path = sys.argv[1]
path="/SalsaBD/Proof"
pathdest = "/SalsaBD/Proof/result"
nworkers = 6

files = []
for root, dirnames, filenames in os.walk(path):
    files.extend(glob.glob(root + "/*.mp3"))
from multiprocessing import Pool
tam = len(files)
i = 0
pool = Pool(processes=nworkers)       # start 4 worker processes

pool.map(procesar,files)

# while i< tam:
#     toproc = files[i:i+nworkers]
#     pool.map(procesar,toproc)
#     print "-"*40
#     step = nworkers
#     if tam-i<nworkers:
#         step = tam-i
#     i+=step
