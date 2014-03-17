# The Collector Sampler / Music Hack Day 2013 Stockholm project #


An industrial-scale sample extraction and playback instrument

Created by [Ragnar Ingi Hrafnkelsson]('http://reactifymusic.com', 'Reactify') and [Owen Hindley]('http://www.owenhindley.co.uk', 'Owen Hindley') for a Music Hack Day in 2013 at Spotify HQ, Stockholm.

## Overview ##


We had the idea of using the [Echonest's]('http://developer.echonest.com/', 'EchoNest') fantastic API to identify strong single-tone samples in audio, and then extract these samples out to use in an instrument. 

The idea being that you can feed in any audio, and produce an sampled instrument that sounds just like that source.



## Creating Samples ##


Samples are generated via a command-line python script, in `/create-samples/analyseFiles.py`.

This script takes a number of arguments:


`-s` (required) The source folder containing the audio you want to convert

`-d` (required) The destination folder where the converted samples will be placed



`-min_avg` (optional, default=`0.2`) The minimum average pitch deviation that results in a valid sample. Lower values will give you more 'clear' single-tone samples, but may result in fewer samples being returned overall.

`-min_duration` (optional, default=`0.2`) in seconds, the minimum duration of a valid sample

`-max_duration` (optional, default=`0.6`) in seconds, the maximum duration of a valid sample

If you had a number of samples (.mp3 is fine) in a folder, say `~/Desktop/mySampleCollection/`, you would process these as follows:

`python analyseFiles.py -s ~/Desktop/mySampleCollection/ -d ~/Desktop/myProcessedSamples/`

Which would use the default values for `min_avg` and `duration` as described above.



## Playing back samples ##


The samples are grouped by notes in the folder specified. 

Also in the filename is a `group` value. This value attempts to group samples by their harmonic content, so that if you play them sequentially, they will 'flow' better. This still needs some work, as the data returned by the Echonest API is (impressively) complex.

You can either insert these files into your own player however you wish, but we've also created some playback tools for instant gratification!

### Web Audio Playback ###

in the folder `webAudioPlayback` you'll find `playback.html`, which allows you to (when run on a local web server) load a folder of samples and play them back both via an on-screen keyboard and your computer's physical keyboard (keys `a` to `j`)

### ofxMaxim Playback (Hack Day project, requires openFrameworks) ###

To use this sample player, make sure to point Xcode to your openFrameworks path. The project has been updated to use the latest (0.8.0) osx release. 

Place the output of the sample generator in bin/Data. Example folder structure:

```
/bin
  /Data
    /Artist Name ("Synth patch" name)
      /A
        *.wav   
      /Bb
        *.wav   
      /B
        *.wav 
      etc.
```
      
The first sample directory is loaded on start. Use keyboard row [ A ] through to [ " ] to play notes. Mouse y position controls filter cutoff and loop length. Each time a note is played, it moves through to the next available sample.

## What's going on ##

### Sample creation & selection process ###

The bulk of the sample creation takes place in `analyseFiles.py`. This in turn requires the use of both the `pyechonest` module and the `remix` modules from [The Echonest.]('http://developer.echonest.com/', 'EchoNest').

The process inside the script is as follows:

- The script searches in the source folder for audio files (`.wav` or `.mp3`)

- The Echonest module then checks these files against their database, to see if this audio track has been analysed before, and if not, uploads it for analysis

- The script then receives an [AudioAnalysis]('http://echonest.github.io/remix/apidocs/echonest.remix.audio.AudioAnalysis-class.html, 'AudioAnalysis') object which describes the audio in terms of bars, beats, 'tatums' (not sure what they are), sections and segments.

- We're interested in segments, so we loop through each one, and examine the following properties:
	
	- Relative strength of a single pitch

		Within each segment, we get an array of pitches, mapped to the chromatic scale. We look at the array, and compare the strength (level) of the highest-ranking pitch to the average of all the other pitches. 

		If the strongest pitch is higher than the `min_avg` parameter, then we take this segment to be sufficiently 'singular' or 'pure' in pitch, and add it to the list of segments that we will later export as samples.

	- Duration of segment

		We check the segment duration to ensure it falls within our `min_duration` and `max_duration` limits.

	- Starting loudness vs average loudness

		We have the option (currently disabled, but you can poke around and re-enable it if you wish) to sort samples by type - either 'shot' type, which start out loud and decrease in volume, or 'pad' samples, which have a pretty even volume throughout. 

	- Timbre

		This is a weird one, and when Paul Lamere tried to explain it to us at 4am on a cold winter night in Stockholm it didn't really sink in. However, basically we think the Echonest uses a 12-dimensional array to represent the harmonic content of the segment. 

		Similar-sounding segments (e.g. containing voice, or strings, drums) should have similar values in their 'timbre' arrays.

		We make a very crude attempt (and this is one of the main areas we want to improve) at grouping samples, or arranging them sequentially by timbre, by calculating the Euclidean distance (kind of the hypotenuse of a 12-dimensional triangle) between a given segment in a note 'group', and a reference sample, which is the first in that group, and sorting them by this value.

		It sort of works, but could be much better!

	- Overall Volume

		We also arrange segments by their maximum volume (`loudness_max`) with respect to the first sample in that group. The intention is that we'll smooth the volume changes between each segment if they are played sequentially (rather than having to normalise each sample)


- Once this process is complete, the samples are written to disk.

- Before the script is complete, however, we also (again, rather crudely) split the groups of files using FFT analysis. Similar to the Timbre property, from the FFT analysis we get an array of frequency 'buckets' from which we can calculate the Euclidean distance to a reference segment (the first one in the group again).

- From this grouping, we add a _group_X_ string to the filenames of the samples (where X is a number) which groups segments with a similar FFT result together, until they reach a `MAX_DEVIATION` value, after which point a new group is created. This group is 'below' the notes grouping, so it's up to the user if they take any notice of it or not.


