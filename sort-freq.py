from scipy.io.wavfile import read,write
import numpy
import sys

signature_freq	= [3107.0514547413791, 3175.0336745689656, 3379.9703663793102, 2964.4867995689656, 3239.3857758620688, 3172.3935883620688, 3786.2136314655172, 2965.1468211206893, 3033.1290409482758, 3034.1190732758619]
signature_len	= len(signature_freq)
min_freq		= 500.
max_freq		= 10000.
rate, data	= read(sys.argv[1]) 

signalsize	= data.size

frq			= numpy.fft.rfftfreq(signalsize, d = 1. / rate)

rfftData	= abs(numpy.fft.rfft(data))

#find first signature_len max freq
maxlist = []
for i in range(10000) :
	max_i = rfftData[1:].argmax() + 1
	if frq[max_i] < min_freq or frq[max_i] > max_freq:
		rfftData = numpy.delete(rfftData, max_i)
		i -= 1
		continue
	maxlist.append(frq[max_i])
	rfftData = numpy.delete(rfftData, max_i)

spectrumtxt	= open("spectrum.txt", 'w')
for fr in maxlist :
	spectrumtxt.write(str(fr) + "\n");
spectrumtxt.close()

#print maxlist
#print numpy.amax(maxlist)
#print numpy.amin(maxlist)
#print frq