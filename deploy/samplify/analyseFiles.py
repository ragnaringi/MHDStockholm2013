from pyechonest import config
import echonest.remix.audio as audio

import argparse
import math
import json
import os

#API key for echonest
config.ECHO_NEST_API_KEY="NMF6CJHDHHDFGO0E8"


#get the folder in which our samples come from
parser = argparse.ArgumentParser(description='Analyse a folder of files.')
parser.add_argument('-s', dest="source_folder",
                   help='a folder containing audio files to analyse')
parser.add_argument('-d', dest="dest_folder",
                   help='a folder where the audio files are output')


args = parser.parse_args()


print "Analysing files in folder : " + args.source_folder

PITCH_LOOKUP = ["A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab"]

ENVELOPE_TYPE_PAD = "pad"
ENVELOPE_TYPE_SHOT = "shot"

outputlist = {}
outputNotes = {}

audio_file = None

i = 0
while i < len(PITCH_LOOKUP):
	pitchName = PITCH_LOOKUP[i]
	outputNotes[pitchName] = []
	outputlist[pitchName] = { ENVELOPE_TYPE_PAD : [], ENVELOPE_TYPE_SHOT : []}
	i += 1

class SampleReference:

	def __init__(self, aSegment, aNote, aEnvelopeType):
		self.segment = aSegment
		self.note = aNote
		self.envelopeType = aEnvelopeType
		self.filename = None
		self.seg_distance = 0

	def exportFile(self, aAudioFile, aIndex):

		global args

		#mark = str(int(self.segment.timbre[0])) + "_" + str(int(self.segment.timbre[1])) + "_" + str(int(self.segment.timbre[2]))
		mark = str(int(self.seg_distance))

		noteFolder = self.note
		destinatonFolder = os.path.abspath(os.path.join(args.dest_folder, noteFolder))

		self.filename = "sample_" + self.note + "_" + str(aIndex).zfill(3) + ".wav"
		destination = os.path.abspath(os.path.join(args.dest_folder + "/" + self.note + "/", self.filename))
		print("saving to path : " + destination)
		self.segment.encode(destination)



def analyseFiles():
	paths = absoluteFilePaths(args.source_folder)
	for path in paths:
		if path.endswith(".mp3") or path.endswith(".wav"):
			processFile(path)


def processFile(aFilePath):
	
	global audio_file

	print "Analysing file :" + aFilePath

	#analyse this track
	print ("...")
	# t = track.track_from_filename(aFilePath, 'mp3', 1)
	# print "Got ID : " + t.id
	audio_file = audio.LocalAudioFile(aFilePath)

	export_segments = []

	print("loaded audio file")
	file_analysis = audio_file.analysis
	segments = file_analysis.segments
	index = 0;
	for segment in segments:
		processSegment(segment)


def processSegment(aSegment):
	
	global outputlist

	note = ""
	envelopeType = ""
	otherPitchAverageStrength = 0
	i = 0
	avg = 0
	while i < len(aSegment.pitches):
		pitchComponent = aSegment.pitches[i]
		if pitchComponent == 1.000:
			note = PITCH_LOOKUP[i]
		else:
			avg += pitchComponent
		i += 1

	avg /= 11

	if (avg < 0.2) and (aSegment.duration > 0.5) and (aSegment.loudness_max > -40):
			print ("found suitable sample, note : " + note)
			
			if ((aSegment.duration / aSegment.time_loudness_max) > 0.25 and (aSegment.loudness_max / aSegment.loudness_begin) < 0.8):
				envelopeType = ENVELOPE_TYPE_SHOT
			else:
				envelopeType = ENVELOPE_TYPE_PAD
			
			newSampleRef = SampleReference(aSegment, note, envelopeType)
			outputNotes[note].append(newSampleRef)


def sortSimilarSamples():
	for note in outputNotes:
		noteGroup = outputNotes[note]
		if (len(noteGroup) > 0):
			referenceSample = noteGroup[0]
		i = 0
		while i < len(noteGroup):
			sample = noteGroup[i]
			seg_distance = 0
			seg_distance = _getEuclideanDistance(sample.segment, referenceSample.segment, 'timbre', 1) * 0.1
			#seg_distance += _getEuclideanDistance(sample.segment, referenceSample.segment, 'pitches', 0) * 10.00
			seg_distance += getVolumeDifference(sample, referenceSample) * 10
			sample.seg_distance = seg_distance
			i += 1
		outputNotes[note] = sorted(noteGroup, key=lambda sample: sample.seg_distance )

  
def getVolumeDifference(aSample, aReferenceSample):
	return (aSample.segment.loudness_max / aReferenceSample.segment.loudness_max)

def _getEuclideanDistance(aObjectA, aObjectB, aField, aWeighted):
	cumulative = 0
	i = 0
	while (i < len(getattr(aObjectA, aField))):
		delta = getattr(aObjectA, aField)[i] - getattr(aObjectB, aField)[i]
		weight = 1.0
		if (aWeighted):
			weight = (1.0 / ((i+1) * 1.0))
		cumulative += delta * delta * weight
		i += 1
    
	return math.sqrt(cumulative)


def exportFiles():

	global audio_file

	for note in outputNotes:
		noteGroup = outputNotes[note]
		index = 0
		for sampleReference in noteGroup:
			sampleReference.exportFile(audio_file, index)
			outputlist[sampleReference.note][sampleReference.envelopeType].append(sampleReference.filename)
			index += 1


def FFTGroupFiles():
	for noteFolder in PITCH_LOOKUP:
		noteFolderPath = os.path.join(args.dest_folder, noteFolder)
		print("grouping files in " + noteFolderPath)
		os.system("python fftGroupSamples.py -s " + noteFolderPath)



def absoluteFilePaths(directory):
   for dirpath,_,filenames in os.walk(directory):
       for f in filenames:
           yield os.path.abspath(os.path.join(dirpath, f))


analyseFiles()
sortSimilarSamples()
exportFiles()

FFTGroupFiles()

sampleListJSON = json.dumps(outputlist)
f = open(os.path.join(args.dest_folder, "samples.json"), 'w')
f.write(sampleListJSON)
f.close()

