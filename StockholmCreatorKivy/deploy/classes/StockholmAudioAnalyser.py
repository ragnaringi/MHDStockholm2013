from pyechonest import config
import echonest.remix.audio as audio

import argparse
import math
import json
import os

from kivy.logger import Logger

config.ECHO_NEST_API_KEY="NMF6CJHDHHDFGO0E8"

PITCH_LOOKUP = ["A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab"]

ENVELOPE_TYPE_PAD = "pad"
ENVELOPE_TYPE_SHOT = "shot"


class StockholmAudioAnalyser:


	def __init__(self, aSourceFolder, aDestFolder, aMinAvg, aMinDuration, aMaxDuration):
		
		self.source_folder = aSourceFolder
		self.dest_folder = aDestFolder
		self.min_avg = aMinAvg
		self.min_duration = aMinDuration
		self.max_duration = aMaxDuration

		self.outputlist = {}
		self.outputNotes = {}

		self.export_segments = []

		self.audio_file = None

		# setup pitch lookup 

		i = 0
		while i < len(PITCH_LOOKUP):
			pitchName = PITCH_LOOKUP[i]
			self.outputNotes[pitchName] = []
			self.outputlist[pitchName] = { ENVELOPE_TYPE_PAD : [], ENVELOPE_TYPE_SHOT : []}
			i += 1




	def analyseFiles(self):

		Logger.info("Analysing files in folder : " + self.source_folder)

		paths = self.absoluteFilePaths(self.source_folder)
		for path in paths:
			if path.endswith(".mp3") or path.endswith(".wav"):
				self.processFile(path)


	def processFile(self, aFilePath):

		Logger.info("Analysing file :" + aFilePath)

		#analyse this track
		Logger.info("...")
		# t = track.track_from_filename(aFilePath, 'mp3', 1)
		# Logger.info "Got ID : " + t.id
		self.audio_file = audio.LocalAudioFile(aFilePath)

		self.export_segments = []

		Logger.info("loaded audio file")
		file_analysis = self.audio_file.analysis
		segments = file_analysis.segments
		index = 0;
		for segment in segments:
			self.processSegment(segment)


	def processSegment(self, aSegment):
		

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

		if (avg < self.min_avg) and (aSegment.duration > self.min_duration) and (aSegment.duration < self.max_duration) and (aSegment.loudness_max > -40):
				Logger.info("found suitable sample, note : " + note)
				
				if ((aSegment.duration / aSegment.time_loudness_max) > 0.25 and (aSegment.loudness_max / aSegment.loudness_begin) < 0.8):
					envelopeType = ENVELOPE_TYPE_SHOT
				else:
					envelopeType = ENVELOPE_TYPE_PAD
				
				newSampleRef = SampleReference(aSegment, note, envelopeType)
				self.outputNotes[note].append(newSampleRef)


	def sortSimilarSamples(self):
		for note in self.outputNotes:
			noteGroup = self.outputNotes[note]
			if (len(noteGroup) > 0):
				referenceSample = noteGroup[0]
			i = 0
			while i < len(noteGroup):
				sample = noteGroup[i]
				seg_distance = 0
				seg_distance = self._getEuclideanDistance(sample.segment, referenceSample.segment, 'timbre', 1) * 0.1
				#seg_distance += _getEuclideanDistance(sample.segment, referenceSample.segment, 'pitches', 0) * 10.00
				seg_distance += self.getVolumeDifference(sample, referenceSample) * 10
				sample.seg_distance = seg_distance
				i += 1
			self.outputNotes[note] = sorted(noteGroup, key=lambda sample: sample.seg_distance )

	  
	def getVolumeDifference(self, aSample, aReferenceSample):
		return (aSample.segment.loudness_max / aReferenceSample.segment.loudness_max)

	def _getEuclideanDistance(self, aObjectA, aObjectB, aField, aWeighted):
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


	def exportFiles(self):

		Logger.info("Checking output folder exists")
		self.checkOutputFolder()

		for note in self.outputNotes:
			noteGroup = self.outputNotes[note]
			index = 0
			for sampleReference in noteGroup:
				sampleReference.exportFile(self.dest_folder, self.audio_file, index)
				self.outputlist[sampleReference.note][sampleReference.envelopeType].append(sampleReference.filename)
				index += 1


	# def FFTGroupFiles():
	# 	for noteFolder in PITCH_LOOKUP:
	# 		noteFolderPath = os.path.join(self.dest_folder, noteFolder)
	# 		Logger.info("grouping files in " + noteFolderPath)
	# 		os.system("python fftGroupSamples.py -s " + noteFolderPath)



	def absoluteFilePaths(self, directory):
	   for dirpath,_,filenames in os.walk(directory):
	       for f in filenames:
	           yield os.path.abspath(os.path.join(dirpath, f))


	def checkOutputFolder(self):
		if os.path.exists(self.dest_folder) is False:
			os.makedirs(self.dest_folder)

		for noteFolder in PITCH_LOOKUP:
			noteFolderPath = os.path.join(self.dest_folder, noteFolder)
			if os.path.exists(noteFolderPath) is False:
				os.makedirs(noteFolderPath)


class SampleReference:

	def __init__(self, aSegment, aNote, aEnvelopeType):
		self.segment = aSegment
		self.note = aNote
		self.envelopeType = aEnvelopeType
		self.filename = None
		self.seg_distance = 0

	def exportFile(self, aDestFolder, aAudioFile, aIndex):

		#mark = str(int(self.segment.timbre[0])) + "_" + str(int(self.segment.timbre[1])) + "_" + str(int(self.segment.timbre[2]))
		mark = str(int(self.seg_distance))

		noteFolder = self.note
		destinatonFolder = os.path.abspath(os.path.join(aDestFolder, noteFolder))

		self.filename = "sample_" + self.note + "_" + str(aIndex).zfill(3) + ".wav"
		destination = os.path.abspath(os.path.join(aDestFolder + "/" + self.note + "/", self.filename))
		Logger.info("saving to path : " + destination)
		self.segment.encode(destination)



# checkOutputFolder()

# analyseFiles()
# sortSimilarSamples()
# exportFiles()

# FFTGroupFiles()

# sampleListJSON = json.dumps(outputlist)
# f = open(os.path.join(self.dest_folder, "samples.json"), 'w')
# f.write(sampleListJSON)
# f.close()

