#!/usr/bin/env python
# Read in a WAV and find the freq's

import wave
import sys
import numpy as np
import matplotlib.pyplot as plt

chunk = 2048

# open up a wave
wf 		= wave.open(sys.argv[1], 'rb')
swidth 	= wf.getsampwidth()
RATE 	= wf.getframerate()

# use a Blackman window
window 	= np.blackman(chunk)

# read some data
data 	= wf.readframes(chunk)

# find the frequency of each chunk
while len(data) == chunk * swidth:
    
    # unpack the data and times by the hamming window
    indata 	= np.array(wave.struct.unpack( "%dh" % ( len(data) / swidth ), data )) * window
    
    # Take the fft and square each value
    fftData 	= abs(np.fft.rfft(indata))**2
    print len(fftData)
    # find the maximum
    which 	= fftData[1:].argmax() + 1
    # use quadratic interpolation around the max
    if which != len(fftData) - 1 :
        #print np.log( fftData[which-1 : which+2 :])
        y0, y1, y2 	= np.log( fftData[which - 1 : which + 2 :])
        x1 		= (y2 - y0) * .5 / (2 * y1 - y2 - y0)

        # find the frequency and output it
        thefreq 	= (which + x1) * RATE / chunk
        print "The freq is %f Hz." % (thefreq)
    else:
        thefreq 	= which * RATE / chunk
        print "The freq is %f Hz." % (thefreq)
    # read some more data
    data 	= wf.readframes(chunk)
