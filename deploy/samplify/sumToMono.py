import os
import shutil

does_packages_exist = 0

current_dir = os.getcwd()
resource_dir = 'packages'
converted_dir = 'packages-converted'
if os.path.exists(converted_dir):
	print 'Removing directory: ' + converted_dir
	shutil.rmtree(converted_dir)

for directory, dirnames, filenames in os.walk(current_dir):
	# Check if 'packages' folder exists
	if os.path.relpath(directory) == resource_dir:
		does_packages_exist = 1

		# Copy 'packages' to resources folder
		print 'Copying ' + resource_dir + ' directory into ' + converted_dir
		shutil.copytree(resource_dir, converted_dir)

		# Convert .aif and .aiff audio files to .wav
		for directory, dirnames, filenames in os.walk(converted_dir):
			for filename in filenames:
				if filename.endswith('.wav') or filename.endswith('wave'):
					if (' ' in filename) or ('\'' in filename):
						print 'Error: spaces or \' not allowed in filename: ' + filename
						continue;
 					inputfile = directory + filename
					inputfile = os.path.relpath(os.path.join(directory, filename))
					outputfile = os.path.relpath(os.path.join(directory, str(filename.split('.')[0] + 'M.wav')))
					os.system("afconvert -f WAVE -d LEI16@44100 -c 1 " + inputfile + " " + outputfile)
					os.remove(inputfile)
					print "Replaced " + inputfile + " with " + outputfile
		break;

if not does_packages_exist:
	print "Could not find \'" + resource_dir + "\' folder"
