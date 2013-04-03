import numpy as np

# from dislin import *
import wave
import sys
import struct

import argparse
import math
import json
import os


#get the folder in which our samples come from
parser = argparse.ArgumentParser(description='Analyse a folder of files.')
parser.add_argument('-s', dest="source_folder",
                   help='a folder containing audio files to analyse')
# parser.add_argument('-d', dest="dest_folder",
#                    help='a folder where the audio files are output')


args = parser.parse_args()

noteAnalysis = []
lastNoteGroup = 0
MAX_DEVIATION = 0.5
currentDeviation = 1.0

print "Analysing files in folder : " + args.source_folder

class sampleFFTReference:

	def __init__(self, aSampleName, aSamplePath, aFFT):
		self.name = aSampleName
		self.path = aSamplePath
		self.fft = aFFT
		self.group = 0
		self.distance = 0


def analyseFiles():
	paths = absoluteFilePaths(args.source_folder)
	for path in paths:
		if path.endswith(".mp3") or path.endswith(".wav"):
			processFile(path)




def processFile(aFilePath):

	print "Analysing file :" + aFilePath

	global noteAnalysis

	fp = wave.open(aFilePath, "rb")
	sample_rate = fp.getframerate()
	data_size=20000

	data = fp.readframes(data_size /4)


	data = struct.unpack("{n}h".format(n=(data_size /2)), data)
	data = np.array(data)

	fp.close()

	w = np.fft.fft(data)
	
	newSampleRef = sampleFFTReference(os.path.basename(aFilePath), aFilePath, w)

	noteAnalysis.append(newSampleRef)

	
def compareNotes():

	global noteAnalysis

	referenceFFT = noteAnalysis[0].fft
	index = 0
	for noteFFT in noteAnalysis:

		noteFFT.distance = _getEuclideanDistance(noteFFT.fft, referenceFFT)
		
	noteAnalysis = sorted(noteAnalysis, key=lambda sample: sample.distance)

	print("compared and sorted notes by FFT distance")


def splitNoteGroups(aGroup):

	global lastNoteGroup

	index = 0

	groupDeviation = 1.0

	i = 0
	cumulative = 0
	cumulativeCount = 0
	highestDelta = 0
	lowestDelta = float("inf")

	while i < len(aGroup):
		noteFFT = aGroup[i]

		if noteFFT.distance != 0 and i < (len(aGroup) -1):
			nextFFT = aGroup[i + 1]

			delta = nextFFT.distance - noteFFT.distance
			if delta > highestDelta:
				highestDelta = delta
			if delta < lowestDelta:
				lowestDelta = delta

			cumulative += delta
			cumulativeCount += 1
		i += 1 

	# get the average delta
	averageDelta = cumulative / cumulativeCount
	print ("averageDelta = " + str(averageDelta))
	print("lowestDelta = " + str(lowestDelta))
	print("highestDelta = " + str(highestDelta))

	groupDeviation = ((lowestDelta / averageDelta) + (averageDelta / highestDelta)) / 2.0
	groupDeviation = 1.0 - groupDeviation
	print("groupDeviation = " + str(groupDeviation))
	print("MAX_DEVIATION = " + str(MAX_DEVIATION))

	if (groupDeviation > MAX_DEVIATION):

		i = 0
		while i < len(aGroup):
			noteFFT = aGroup[i]
			
			if noteFFT.distance != 0 and i < (len(aGroup) -1):
				nextFFT = aGroup[i + 1]

				delta = nextFFT.distance - noteFFT.distance

				print("delta : " + str(delta))
				
				if (delta > averageDelta):
					print("splitting group..")
					lastNoteGroup += 1

			noteFFT.group = lastNoteGroup
			print(noteFFT.name + " is now in group" + str(noteFFT.group))
			i += 1 

	# RENAMING
	
	
	for noteFFT in noteAnalysis:
		os.rename(noteFFT.path, noteFFT.path.replace("sample_", "group_" + str(noteFFT.group) + "_sample_"))
		
	


def _getEuclideanDistance(aObjectA, aObjectB):
	cumulative = 0
	i = 0
	while (i < len(aObjectA)):
		delta = aObjectA[i].real - aObjectB[i].real
		weight = 1.0
		cumulative += delta * delta * weight
		i += 1
    
	return math.sqrt(cumulative)











def absoluteFilePaths(directory):
   for dirpath,_,filenames in os.walk(directory):
       for f in filenames:
           yield os.path.abspath(os.path.join(dirpath, f))


analyseFiles()
compareNotes()
splitNoteGroups(noteAnalysis)

