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
