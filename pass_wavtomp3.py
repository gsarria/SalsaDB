from pydub import AudioSegment
import taglib

import os
import glob
import sys
import md5
from multiprocessing import Pool

def procesar(filename):
    fname = filename.split('/')[-1]
    # foutname = "%s/%s.mp3" % (pathdest,md5.md5(fname).hexdigest())
    # print "%s -> %s.mp3" % (fname,foutname)
    # fin = open(filename,"r")
    # fout = open(foutname,"w")
    # fout.write(fin.read())
    # fin.close()
    # fout.close()
    fn=fname[0:len(fname)-4]+".wav"
    fn=path+'/'+fn
    print filename+" ========== "+fn
    sound = AudioSegment.from_wav(fn)
    tag1=taglib.File(filename)
    sound.export(filename)
    tag2=taglib.File(filename)
    tag2.tags=tag1.tags
    tag2.save()
    # pat=pathcopy+fname
    # os.rename(filename,pat);
    # s=md5.md5(filename).hexdigest()+".mp3"
    # ss=md5.md5(filename).hexdigest()+".wav"
    # dirr=pathdest+fname
    # os.rename(s,fname)
    # os.remove(ss)


# path = sys.argv[1]
# path="/home/gsarria/salsaDB/BDMusica"
path="/SalsaBD/ChorusResults"
#pathcopy="/vol-users/gsarria/BDMusica_ok/"
# pathcopy="vol-users/gsarria/BDMusica_ok_MP3/"
#pathdest = "/home/gsarria/salsaDB/Resultado/"
# pathdest = "/vol-users/gsarria/"
nworkers = 4

files = []
for root, dirnames, filenames in os.walk(path):
    files.extend(glob.glob(root + "/*.mp3"))
from multiprocessing import Pool
tam = len(files)
i = 0
pool = Pool(processes=nworkers)       # start 4 worker processes

pool.map(procesar,files,10)