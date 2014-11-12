from essentia.standard import *
from pylab import plot, show, figure
from numpy.linalg import norm
import array
import time
import numpy as np
from scipy import signal
from scipy.signal import argrelmax
import librosa
import sys 
import eyed3 ##de aqui empiezan solo librerias para reconocer los tags...
#import id3
import songdetails
import os
import taglib ## <<<<--------
import audiotools ## hasta aqui
from pydub import AudioSegment
import md5
import wave

class SignalProc:
    audio=[]
    normales=[]
    framePool=[]
    coros=[]
    numframes=0
    points=0
    points_per_secound=0
    metadata=[]
    frames_correlation=[]
    mRepeated=[]

    positions=[]

    #Creator
    #input: filename
    def __init__(self, data):
            self.fn = data
            self.extractRawSignal(self.fn)

    
    #Load audio
    #input: filename
    def extractRawSignal(self, fn):
            loader = essentia.standard.MonoLoader(filename = fn)
            self.metadata=essentia.standard.MetadataReader(filename= fn )()[:-1]
            self.audio = loader()
            self.points=len(self.audio)
            self.points_per_secound=self.points/self.metadata[7]
            #Down sampling
            ffn=md5.md5(fn).hexdigest()
            # print ffn
            fnn=ffn+".wav"
            # print fnn
            print "Sampling Down..."
            librosa.output.write_wav(fnn,self.audio,44100)
            sound = AudioSegment.from_wav(fnn)
            sound.export(fnn, format="wav", bitrate="32k")
            loader = essentia.standard.MonoLoader(filename = fnn)
            self.audio = loader()
            print "Sampling Down Ok!"

    #Separate audio
    #input: audio file, treshold(se refiere mas que todo a la amplitud), size (0<size<=1)

    # def getFrames(self, audio, treshold, size):
    def getFrames(self, treshold, size):
            peaks = argrelmax(self.audio)[0]
            framesize = int(len(self.audio)*size)
            for fstart in peaks:          
                    if self.audio[fstart]<treshold:
                        continue
                    frame = self.audio[fstart:min(fstart+framesize,len(self.audio))]
                    # self.positions.append(fstart)
                    nf = norm(frame)
                    # print nf
                    if nf>0:
                        self.framePool.append(frame)
                        self.normales.append(nf)
                        self.positions.append(fstart)
            self.numframes=len(self.framePool)

    #Cross-correlation
    #input: vectors
    #def crossCor(self,x,y):
    #        return fftshift(ifft(conjugate(fft(np.concatenate([x,np.array(array.array('i',(0,)*(len(y)-1)))])))*fft(np.concatenate([y,np.array(array.array('i',(0,)*(len(x)-1)))]))))
    
    #If considered same
    #input: vectors
    def same(self,x,y,nx,ny):
            rxcorr = max(signal.fftconvolve(x,y[::-1],mode='full')) / (nx*ny)
            if rxcorr > 0.95:	#similitude of 0.95
                    return True
            else:
                    return False
    
    #Positions of the most repeated frames
    #input: frames repeated vector
    def maxPos(self,r):
            mx = r[0]
            mxpos = [0]
            for i in range(1, len(r)):
                    if r[i] > mx:
                            mx=r[i]
                            mxpos = [i]
                    elif r[i] == mx:
                            mxpos.append(i)
            return mxpos
    
    #Extract possible chorus frames
    #input: audio file, treshold, size (0<size<=1)
    #output: vector with most frames repeated

    #def getChorus(self, treshold, size):
    def getChorus(self):
            # audio = self.extractRawSignal(self.fn)
            # self.getFrames(audio, treshold, size)
            repeated = array.array('i',(0,)*len(self.framePool))
            co=[]
            d=0
            for i in range(0,len(self.framePool)):
                co.append([0])
            for i in range(0, len(self.framePool)):
                    # if repeated[i] > 0:
                    #         continue
                    for j in range(i+1, len(self.framePool)):
                            # if repeated[j] > 0:
                            #     continue
                            if self.same(self.framePool[i],self.framePool[j],self.normales[i],self.normales[j]):
                                    # repeated[i]+=1
                                    # repeated[j]+=1
                                    co[i].append(d)
                                    co[j].append(d)
                            d=d+1
##            self.coros = self.maxPos(repeated)
##            return self.coros
            self.frames_correlation=co
            # self.repe=repeated
##            return repeated
            return co

#search in output getChourus the vector most repeated
#input: vector c with most repeated
#output: frame with posible chorus
    def mostrepeated(self):
        u=0
        p=0
        b=False
        car=0
        tmpu=0
        tmpc=0
        le=0
        uu=0
        pp=0
        lee=0
        for i in range(len(self.frames_correlation)):
            tmpc=len(self.frames_correlation[i])-1
            if tmpc>=le and self.positions[i]+self.points_per_secound*10<len(self.audio):
                le=tmpc
                #u=i
                p=i
                u=self.positions[i]
            if tmpc>lee and self.positions[i]+self.points_per_secound*10<len(self.audio):
                lee=tmpc
                #uu=i
                pp=i
                uu=self.positions[i]
        # if u==len(self.frames_correlation)-1 or u==len(self.frames_correlation):
        # print len(self.frames_correlation)
        # print p
        if p==len(self.frames_correlation)-1 or p==len(self.frames_correlation):
            self.mRepeated=[uu,lee]
            # print ":O"
        else:
            # print ":D"
            self.mRepeated=[u,le]
        # print self.mRepeated[0]
        # print self.mRepeated[1]
        # self.mRepeated=[]
        # self.mRepeated=[p,le] 

    #Print the possible chorus frames
    #input: null

    def printFrames(self):
##        for i in self.coros:
        for i in self.repe:
            plot(self.framePool[i])
            show()
    ## build to mp3 file with 10 sec to chorus and metadata   
    def outputAudio(self,filename,location,fname):
       loader = essentia.standard.MonoLoader(filename =  filename)
       self.audio = loader()
       aver=[]
       # for x in range(int((self.points/len(self.framePool))*self.mRepeated[0]),int((self.points/len(self.framePool))*self.mRepeated[0]+self.points_per_secound*10)):
       # for x in range(self.mRepeated[0],int(self.mRepeated[0]+self.points_per_secound*10)):
       #     aver.append(self.audio[x])
       aver=self.audio[self.mRepeated[0]:self.mRepeated[0]+self.points_per_secound*10]
       ffn=md5.md5(filename).hexdigest()
       # print ffn
       fnn=ffn+".wav"
       # print fnn
       ffn=ffn+".mp3"
       # print ffn
       librosa.output.write_wav(fnn,aver,44100)
       sound = AudioSegment.from_wav(fnn)
       ffn=fname
       # ffn=location+'/'+'t'+ffn
       ffn=location+'/'+ffn
       print "location mp3 process"
       print ffn
       sound.export(ffn, format="mp3")

       tag1=taglib.File(filename)
       tag2=taglib.File(ffn)

       tag2.tags=tag1.tags
       tag2.save()
       
       ## intentos con la metadata...

       # track= audiotools.open(sys.argv[1])
       # track2=audiotools.open("asdf.mp3")

       #track=audiotools.open(sys.argv[1])

       #meta=track.get_metadata()
       #track2.update_metadata(meta)

       # song=songdetails.scan(sys.argv[1])
       # song2=songdetails.scan(sys.argv[1])
       # song2=song
       # song2.save()

       # tag=eyed3.load(sys.argv[1])
       # tag2=eyed3.load("asdf.mp3")
       # print tag2.tag.artist
       # tag2=tag
       # print tag2.tag.artist
       # tag2.tag.save()

       # tag2.setTitle(self.metadata[0])
       # tag2.setArtist(self.metadata[1])
       # tag2.setAlbum(self.metadata[2])
       # tag2.setComments(self.metadata[3])
       # tag2.setGenre(self.metadata[4])
       # tag2.setTrack(self.metadata[5])
       # tag2.setYear(self.metadata[6])
       # tag2.setLength(self.metadata[7])
       # tag2.setBibrate(self.metadata[8])
       # tag2.setSampleRate(self.metadata[9])
       # tag2.setChannels(self.metadata[10])
       
       
       # essentia.standard.MonoWriter(filename = 'sample.mp3')(aver)
def process(filename,location,fname):
    #testing
    start_time = time.time()
    #Get the object that have the signal properties, the parameter is the name of the file, can be mp3 or wav
    x = SignalProc(filename)
    #get the chorus frames, the parameters are the treshold to be considered a peak and
    #the size of the frame, the beat is not extracted

    ## proof tags
    # tag1=taglib.File(sys.argv[1])
    # print tag1.tags

    z=ReplayGain()(x.audio)
    # print z
    # print 11.5-abs(z)
    f=11.5
    if f-abs(z)>0:
        # print 10**((11.5-abs(z))/20)
        facc=10**((f-abs(z))/20)
        # fac=20*np.log10(13-abs(z))
        # print fac
        # facc=((13-abs(z))*2)/6.020599913
        # print facc
        # # x.audio=Scale(factor = 10**((abs(z))/20))(x.audio)
        x.audio=Scale(factor = facc )(x.audio)
        print "amplify ok!"
    #x.audio = librosa.logamplitude(x.audio, ref_power=facc)
    # print "converti"

    # aver=[]
    # aver=x.audio[0:len(x.audio)-1]
    # librosa.output.write_wav('tmpp.wav',aver,44100)

    # print ReplayGain()(x.audio)

    # print ReplayGain()(x.audio)

    # for i in x.audio:
    #     db_value = 20 * np.log10( i )
    #      i = 10 ** ( db_value / 20 )

    # pe=StrongPeak()(x.audio)
    # print pe
    # print 20*np.log10(pe)





    x.getFrames(0.95, 0.001)
    c=x.getChorus()
    x.mostrepeated()
    if x.mRepeated[0]==0:
        print "check 1"
        x.framePool=[]
        x.normales=[]
        x.positions=[]
        x.getFrames(0.90,0.001)
        c=x.getChorus()
        x.mostrepeated()
        if x.mRepeated[0]==0:
            print "check 2"
            x.framePool=[]
            x.normales=[]
            x.positions=[]
            x.getFrames(0.85,0.001)
            c=x.getChorus()
            x.mostrepeated()
            if x.mRepeated[0]==0:
                print "check 3"
                x.framePool=[]
                x.normales=[]
                x.positions=[]
                x.getFrames(0.80,0.001)
                c=x.getChorus()
                x.mostrepeated()
                if x.mRepeated[0]==0:
                    print "check 4"
                    x.framePool=[]
                    x.normales=[]
                    x.positions=[]
                    x.getFrames(0.75,0.001)
                    c=x.getChorus()
                    x.mostrepeated()
                    if x.mRepeated[0]==0:
                        print "check 5"
                        x.framePool=[]
                        x.normales=[]
                        x.positions=[]
                        x.getFrames(0.70,0.001)
                        c=x.getChorus()
                        x.mostrepeated()
                        if x.mRepeated[0]==0:
                            print "check 6"
                            x.framePool=[]
                            x.normales=[]
                            x.positions=[]
                            x.getFrames(0.65,0.001)
                            c=x.getChorus()
                            x.mostrepeated()
                            if x.mRepeated[0]==0:
                                print "check 7"
                                x.framePool=[]
                                x.normales=[]
                                x.positions=[]
                                x.getFrames(0.60,0.001)
                                c=x.getChorus()
                                x.mostrepeated()
                                if x.mRepeated[0]==0:
                                    print "check 8"
                                    x.framePool=[]
                                    x.normales=[]
                                    x.positions=[]
                                    x.getFrames(0.55,0.001)
                                    c=x.getChorus()
                                    x.mostrepeated()
                                    if x.mRepeated[0]==0:
                                        print "check 9"
                                        x.framePool=[]
                                        x.normales=[]
                                        x.positions=[]
                                        x.getFrames(0.50,0.001)
                                        c=x.getChorus()
                                        x.mostrepeated()
                                        if x.mRepeated[0]==0:
                                            print "check 10"
                                            x.framePool=[]
                                            x.normales=[]
                                            x.positions=[]
                                            x.getFrames(0.45,0.001)
                                            c=x.getChorus()
                                            x.mostrepeated()
                                            if x.mRepeated[0]==0:
                                                print "check 11"
                                                x.framePool=[]
                                                x.normales=[]
                                                x.positions=[]
                                                x.getFrames(0.40,0.001)
                                                c=x.getChorus()
                                                x.mostrepeated()   
    # print c      
    # x.mostrepeated()
    x.outputAudio(filename,location,fname)
    #plot the frames obtained of the chorus
    #x.printFrames()
    #the elements in vector c are the integers of the frame pool in x
    ##print x.framePool[c[102]]
    #x.outputAudio()
    #plot(x.framePool[1])
    #show()
    #plot(x.framePool[2])
    #show()
    ##print x.framePool[c[85]]
    ##print x.framePool[c[2]]
    ##print x.framePool[c[3]]
    ##print x.framePool[c[4]]
    tim=time.time() - start_time
    if tim>10:
        f = open('log.txt','a')
        lo= filename + "    time:" +str(tim)+"\n"
        f.write(lo)
        f.close()
    print time.time() - start_time, "seconds"

# process(sys.argv[1],"/Users/gsarria/Dropbox/Research/SalsaDb/Software",sys.argv[1])
