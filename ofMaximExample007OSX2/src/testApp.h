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
    
        int selectedKey;
        void playNote (string key, int index);
        void loadNote (string key, int index);
	
		int		initialBufferSize; /* buffer size */
		int		sampleRate;
	
		/* stick you maximilian stuff below */
	
		double leftOutput, rightOutput ,outputs[2];
        double outVolume;
    
        int playbackLenght;
        double playbackSpeed;
        double cutoff;
        double resonance;
        int delayTime;
        string currentSamplePath;
		
        ofxMaxiSample sample[11];
        ofxMaxiSample *currentSample;
        ofxMaxiMix mymix;
        maxiEnv env;
        maxiDelayline delay;
        maxiEnvelope myEnvelope;
        maxiFilter myFilter;
    
        int sampleNumber;
        bool playSample;
        vector<ofFile>samplePaths;
};
