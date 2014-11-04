#Detects noise and starts recoring accordingly

import alsaaudio, wave, numpy, sys
from scipy.io.wavfile import read,write

inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE)
inp.setchannels(1)
inp.setrate(44100)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
inp.setperiodsize(1024)

fname = sys.argv[1]
w = wave.open(fname, 'w')
w.setnchannels(1)
w.setsampwidth(2)
w.setframerate(44100)

noise = wave.open("noise.wav", 'w')
noise.setnchannels(1)
noise.setsampwidth(2)
noise.setframerate(44100)

b_noise 	= True
prev_db 	= 0
threshold 	= 200

while True:
    l, data = inp.read()
    a = numpy.fromstring(data, dtype='int16')
    curr_db = numpy.abs(a).mean()

    print curr_db

    if prev_db == 0:
    	prev_db = curr_db
    elif curr_db - prev_db > threshold:
    	b_noise = False

    if b_noise:
    	noise.writeframes(data)
    else:
    	print "rec"
    	w.writeframes(data)
noise.close()
w.close()

nrate, noiseData	= read("noise.wav")
wrate, recData		= read(fname)

rfftNoise			= numpy.fft.rfft(noiseData)
rfftRec				= numpy.fft.rfft(recData)