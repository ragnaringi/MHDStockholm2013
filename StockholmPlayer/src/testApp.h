#pragma once

#include "ofMain.h"
#include "ofxMaxim.h"

class testApp : public ofBaseApp{

	public:
		~testApp();
		void setup();
		void update();
		void draw();
		void keyPressed  (int key);
		void keyReleased(int key);
		void mouseMoved(int x, int y );
	
		void audioRequested (float * input, int bufferSize, int nChannels);
		void audioReceived 	(float * input, int bufferSize, int nChannels);
    
        int selectedKey;
        string notePlaying;
        void playNote (string key, int index);
        void loadNote (string key, int index);
        void loadSynthPatch();
        string synthpatch;
        string currentSamplePaths[11];
    
        ofTrueTypeFont font;
	
		/* Maximilian */
	
		double leftOutput, rightOutput, outputs[2];
        double outVolume;
    
        bool shouldPlay;
        int playbackLength;
        double playbackSpeed;
        double cutoff;
		
        ofxMaxiSample sample[11];
        ofxMaxiSample *currentSample;
        maxiEnvelope envelope;
        maxiFilter filter;
        ofxMaxiMix mainMix;
};
