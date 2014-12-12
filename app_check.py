import pyaudio  
import wave  
import random
import os
import glob
import sys
# import md5
# from multiprocessing import Pool
repro=False
# path="/Users/gsarria/Dropbox/Research/SalsaDb/Software/app" #direccion de los wav's
path="/SalsaBD/ChorusResults"  ##direccion de los wav's 
files = []
ex=False
ff=[]
coros=0
partcoros=0
nocoros=0
co=0
resq=[]
for root, dirnames, filenames in os.walk(path):
    files.extend(glob.glob(root + "/*.wav"))

def reproducir(filename):
	#filename=files[num]
	fname=filename.split('/')[-1]
	print "cancion "+fname
	#define stream chunk   
	chunk = 1024  

	#open a wav format music  
	# f = wave.open(r"Ah_Ah_Oh_No.wav","rb")
	f = wave.open(filename,"rb")  
	#instantiate PyAudio  
	p = pyaudio.PyAudio()  
	#open stream  
	stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
	                channels = f.getnchannels(),  
	                rate = f.getframerate(),  
	                output = True)  
	#read data  
	data = f.readframes(chunk)  

	#paly stream  
	while data != '' and repro==False:  
	    stream.write(data)  
	    data = f.readframes(chunk)  

	#stop stream  
	stream.stop_stream()  
	stream.close()  

	#close PyAudio  
	p.terminate()

def checkfile(archivo):  
    if os.path.exists(archivo): 
        return True
    else: 
        return False


def upwake():
	resq=[]
	f=open('result','r')
	resq.append(int(f.readline()))
	resq.append(int(f.readline()))
	resq.append(int(f.readline()))
	f.close()
	f=open('tmp','r')
	resq.append(0)
	for line in f:
		if int(line)==1:
			# ff.append(True)
			resq.append(True)
			resq[3]=resq[3]+1
		else:
			# ff.append(False)
			resq.append(False)
	f.close()
	print "rescatado..."
	return resq

def grabar():
	f = open('result','w')
	lo= str(coros)+ " \n"
	f.write(lo)
	lo= str(partcoros)+ " \n"
	f.write(lo)
	lo= str(nocoros)+ " \n"
	f.write(lo)
	f.close()
	f = open('tmp','w')
	for x in range(0,len(ff)-1):
		if ff[x]==True:
			f.write(str(1)+" \n")
		else:
			f.write(str(0)+" \n")
	f.close()

for x in range(0,len(files)-1):
  	ff.append(False) 

if checkfile("tmp"):
	resq=upwake()
	coros=resq[0]
	partcoros=resq[1]
	nocoros=resq[2]
	co=resq[3]
	ff=resq[4:len(resq)-1]
# m=False 
if co==0:
	co=1
for x in range(co,375):
	if ex:
		break
	# if m==False and co!=0:
	# 	m=True
	# 	x=co
	y=random.randrange(17960)
	print "Cancion numero "+ str(x)
	while 1:
		if ff[y]==True:
			y=random.randrange(17960)
		else:
			break
	reproducir(files[y])
	print "Que le parece a usted?"
	print "1: Es coro"
	print "2: Tiene parte de un coro"
	print "3: No, en definitiva no es un coro"
	print "4: Escuchar de nuevo la cancion"
	print "0: salir!"
	while True:
	    try:
	        z = int(raw_input("Ingrese su deciscion number: "))
	        if z==0:
	        	print "grabando..."
	        	grabar()
	        	print "grabado ok!"
	        	ex=True
	        	break
	        elif z==1:
	        	coros=coros+1
	        	break
	        elif z==2:
	        	partcoros=partcoros+1
	        	break
	        elif z==3:
	        	nocoros=nocoros+1
	        	break
	        elif z==4:
	        	reproducir(files[y])
	        	print "Que le parece a usted?"
			print "1: Es coro"
			print "2: Tiene parte de un coro"
			print "3: No, en definitiva no es un coro"
			print "4: Escuchar de nuevo la cancion"
	        	continue
	        else:
	        	print "Ingrese una opcion valida"
	        	continue
	    except ValueError:
	        print "Ingrese por favor un numero..."
	 	if ex:
	 		break
	ff[y]=True
if ex!=True:
	grabar()
	print "finalizado"
	print "grabado ok!"

