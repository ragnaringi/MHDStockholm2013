#pragma once

#include "ofMain.h"
#include "ofxMaxim.h"


class testApp : public ofBaseApp{

	public:
		~testApp();/* destructor is very useful */
		void setup();
		void update();
		void draw();

		void keyPressed  (int key);
		void keyReleased(int key);
		void mouseMoved(int x, int y );
		void mouseDragged(int x, int y, int button);
		void mousePressed(int x, int y, int button);
		void mouseReleased(int x, int y, int button);
		void windowResized(int w, int h);
		void dragEvent(ofDragInfo dragInfo);
		void gotMessage(ofMessage msg);
	
		void audioRequested 	(float * input, int bufferSize, int nChannels); /* output method */
		void audioReceived 	(float * input, int bufferSize, int nChannels); /* input method */
	
		int		initialBufferSize; /* buffer size */
		int		sampleRate;
	
		/* stick you maximilian stuff below */
	
		double leftOutput, rightOutput ,outputs[2];
        double outVolume;
        double cutoff;
        double resonance;
        int delayTime;
		
        ofxMaxiSample sample;
        ofxMaxiMix mymix;
        maxiEnv env;
        maxiDelayline delay;
        maxiEnvelope myEnvelope;
        maxiFilter myFilter;
    
        int sampleNumber;
        bool playSample;
        vector<ofFile>samplePaths;
};
