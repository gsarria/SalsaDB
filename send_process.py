#!/usr/bin/python

import os
import glob
import sys
import md5
from multiprocessing import Pool
import taglib
import send_choruExtractor

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
    send_choruExtractor.process(filename,pathdest,fname)
    pat=pathcopy+fname
    os.rename(filename,pat);
    # s=md5.md5(filename).hexdigest()+".mp3"
    # ss=md5.md5(filename).hexdigest()+".wav"
    # dirr=pathdest+fname
    # os.rename(s,fname)
    # os.remove(ss)


# path = sys.argv[1]
# path="/home/gsarria/salsaDB/BDMusica"
path="/vol-users/gsarria/BDMusica"
#pathcopy="/vol-users/gsarria/BDMusica_ok/"
pathcopy="vol-users/gsarria/BDMusica_ok_MP3/"
#pathdest = "/home/gsarria/salsaDB/Resultado/"
pathdest = "/vol-users/gsarria/"
nworkers = 60

files = []
for root, dirnames, filenames in os.walk(path):
    files.extend(glob.glob(root + "/*.MP3"))
from multiprocessing import Pool
tam = len(files)
i = 0
pool = Pool(processes=nworkers)       # start 4 worker processes

pool.map(procesar,files,10)

#n = tam/(nworkers*10)

#for f in files:
#	procesar(f)
#	print "> Done",f

#for x in pool.imap(procesar,files,n):
#   print "----------------- FINALIZADO PROCESO -------------------"

# while i< tam:
#     toproc = files[i:i+nworkers]
#     pool.map(procesar,toproc)
#     print "-"*40
#     step = nworkers
#     if tam-i<nworkers:
#         step = tam-i
#     i+=step
