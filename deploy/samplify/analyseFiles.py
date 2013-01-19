from pyechonest import config
import echonest.remix.audio as audio

import argparse
import os

#API key for echonest
config.ECHO_NEST_API_KEY="NMF6CJHDHHDFGO0E8"


#get the folder in which our samples come from
parser = argparse.ArgumentParser(description='Analyse a folder of files.')
parser.add_argument('-source', dest="source_folder",
                   help='a folder containing audio files to analyse')
parser.add_argument('-destination', dest="dest_folder",
                   help='a folder where the audio files are output')


args = parser.parse_args()
outputIndex = 0;
print "Analysing files in folder : " + args.source_folder

PITCH_LOOKUP = ["A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab"]


def analyseFiles():
	paths = absoluteFilePaths(args.source_folder)
	for path in paths:
		if path.endswith(".mp3"):
			processFile(path)


def processSegment(aSegment):
	
	global outputIndex

	note = ""
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

	if (avg < 0.1):
		if (aSegment.duration > 0.5):
			print ("found suitable sample, note : " + note)
			newFileName = "sample_" + note + "_" + str(outputIndex) + ".mp3"
			aSegment.encode(os.path.abspath(os.path.join(args.dest_folder, newFileName)))
			outputIndex += 1





def processFile(aFilePath):
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


	




def absoluteFilePaths(directory):
   for dirpath,_,filenames in os.walk(directory):
       for f in filenames:
           yield os.path.abspath(os.path.join(dirpath, f))



analyseFiles()

