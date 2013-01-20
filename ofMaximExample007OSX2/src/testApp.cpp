/* This is an example of how to integrate maximilain into openFrameworks, 
 including using audio received for input and audio requested for output.
 
 
 You can copy and paste this and use it as a starting example.
 
 */


#include "testApp.h"


double myEnvelopeData[8] = {0,0,1,500,1,500,0,500};//this data will be used to make an envelope. Value and time to value in ms.

// Vector with allowed key values
static const int keyValues[11] = {97,115,100,102,103,104,106,107,108,59,39}; // 92};
vector<int> keyInputs (keyValues, keyValues + sizeof(keyValues) / sizeof(keyValues[0]) );

static const string notes[11] = {"A", "Bb", "B", "C", "Db", "Eb", "E", "F", "Gb", "G"}; // "Ab"};
//vector<int> keyInputs (keyValues, keyValues + sizeof(keyValues) / sizeof(keyValues[0]) );

string synthpatch  = "SigurRos";

//-------------------------------------------------------------
testApp::~testApp() {
	
    for (int i = 0; i < 11; i++) {
        delete sample[i].myData;
    }
	 /*you should probably delete myData for any sample object
						 that you've created in testApp.h*/
	
}


//--------------------------------------------------------------
void testApp::setup(){
	/* some standard setup stuff*/
	
	ofEnableAlphaBlending();
	ofSetupScreen();
	ofBackground(0, 0, 0);
	ofSetVerticalSync(true);
	
	/* This is stuff you always need.*/
	
	sampleRate 			= 44100; /* Sampling Rate */
	initialBufferSize	= 1024;	/* Buffer Size. you have to fill this buffer with sound*/
	
	/* Now you can put anything you would normally put in maximilian's 'setup' method in here. */
	
    //some path, may be absolute or relative to bin/data
    string path = ofToDataPath(synthpatch);
    
    for (int i = 0; i < 11; i++) {
        path += "/" + notes[i];
        ofDirectory dir(path);
        //only show wav files
        if (dir.exists()) {
            //cout << "woohoo" << endl;
            dir.allowExt("wav");
            //populate the directory object
            dir.listDir();
            samplePaths = dir.getFiles();
            
            sample[i].load(samplePaths[0].path());
            sample[i].getLength();
        }
    }

    sampleNumber = 0;
    playSample = false;
    playbackLenght = 1;
    
    myEnvelope.amplitude=myEnvelopeData[0]; //initialise the envelope
    cutoff = 0.9;
    delayTime = 1;
    
    currentSample = &sample[0];
    currentSamplePath = currentSample->myPath;
    
	ofSoundStreamSetup(2,0,this, sampleRate, initialBufferSize, 4);/* Call this last ! */
}

//--------------------------------------------------------------
void testApp::update(){
	
}

//--------------------------------------------------------------
void testApp::draw(){
	
	/* You can use any of the data from audio received and audiorequested to draw stuff here.
	 Importantly, most people just use the input and output arrays defined above.
	 Clever people don't do this. This bit of code shows that by default, each signal is going to flip
	 between -1 and 1. You need to account for this somehow. Get the absolute value for example.
	 */
	
	ofSetColor(255, 255, 255,255);
	ofRect(300, 300, leftOutput*150, leftOutput*150); /* audio sigs go between -1 and 1. See?*/
    ofRect(600, 300, rightOutput*150, rightOutput*150); /* audio sigs go between -1 and 1. See?*/
	
}

//--------------------------------------------------------------
void testApp::audioRequested 	(float * output, int bufferSize, int nChannels){
	
	for (int i = 0; i < bufferSize; i++){
		
		/* Stick your maximilian 'play()' code in here ! Declare your objects in testApp.h.
		 */
		if (playSample) {
            outVolume = myEnvelope.line(6,myEnvelopeData);
            leftOutput = currentSample->play(1.0, 0, currentSample->length);
        }
        else {
            leftOutput = 0;
        }
        
        
        if (currentSample->position >= (currentSample->length/(double)playbackLenght) - 1) {
    
            currentSample->position = 0;
        }
        
        leftOutput = myFilter.lores(leftOutput, cutoff, 4.0);
        leftOutput *= outVolume;

        double delayOut = delay.dl(leftOutput, int(currentSample->length-1)/playbackLenght, 0.6);
        
		mymix.stereo(leftOutput + delayOut, outputs, 0.5);
		
		output[i*nChannels    ] = outputs[0]; /* You may end up with lots of outputs. add them here */
		output[i*nChannels + 1] = outputs[1];
	}
	
}

//--------------------------------------------------------------
void testApp::audioReceived (float * input, int bufferSize, int nChannels){	
	
	/* You can just grab this input and stick it in a double, then use it above to create output*/
	
	for (int i = 0; i < bufferSize; i++){
		
		/* you can also grab the data out of the arrays*/
	}
	
}

void testApp::playNote(string key, int index) {
    
    sample[index].getLength();
    currentSample = &sample[index];
    
    delay.memory[currentSample->length];
        
    sampleNumber++;
    
    //Attack time
    myEnvelopeData[3] = (double)(currentSample->length/16) / 44.1;
    //Sustain time
    myEnvelopeData[5] = (currentSample->length/2) / 44.1;
    //Release time
    myEnvelopeData[7] = (currentSample->length/16) / 44.1;
    
    if (sampleNumber >= samplePaths.size() - 1) {
        sampleNumber = 0;
    }
    
    playSample = true;
    
    myEnvelope.trigger(0,myEnvelopeData[0]);
}

void testApp::loadNote(string key, int index) {
    
    string path = ofToDataPath(synthpatch);
    
    path += "/" + key;
    ofDirectory dir(path);
    //only show wav files
    
    if (dir.exists()) {
        //cout << "woohoo" << endl;
        dir.allowExt("wav");
        //populate the directory object
        dir.listDir();
        samplePaths = dir.getFiles();
        cout << sample[index].myPath;
        // find the index of current sample in this directory
        sampleNumber = 0;
        for (size_t i = 0; i < samplePaths.size(); i++)
        {
            if (sample[index].myPath == samplePaths[i].path()) {
                sampleNumber = (int)i;
                //cout << sampleNumber << endl;
            } else {
                //sampleNumber = 1;
            }
        }
        
        sampleNumber++;
        if (sampleNumber >= samplePaths.size() - 1) {
            sampleNumber = 0;
        }
        
        currentSamplePath = samplePaths[sampleNumber].path();
        //cout << "sample path: " << currentSamplePath << endl;
        
        sample[index].load(currentSamplePath);
        sample[index].getLength();
        currentSample = &sample[index];
        
        delay.memory[currentSample->length];
        
        playSample = true;
    }
    
    //Attack time
    myEnvelopeData[3] = (double)(currentSample->length/16) / 44.1;
    //Sustain time
    myEnvelopeData[5] = (currentSample->length/2) / 44.1;
    //Release time
    myEnvelopeData[7] = (currentSample->length/16) / 44.1;
    
    myEnvelope.trigger(0,myEnvelopeData[0]);
}

//--------------------------------------------------------------
void testApp::keyPressed(int key){
    
    int index = -1;
	if (std::find(keyInputs.begin(), keyInputs.end(), key) != keyInputs.end())
    {
        
        if (!playSample && selectedKey != key) {
            selectedKey = key;
            //cout << selectedKey << endl;
            
            // find the index of key on keyboard
            for (size_t i = 0; i < keyInputs.size(); i++)
            {
                if (keyInputs[i] == key)
                    index = (int)i;
            }
            playNote(notes[index], 0);
        }
    }
}

//--------------------------------------------------------------
void testApp::keyReleased(int key){

	playSample = false;
    
    int index = -1;
	if (std::find(keyInputs.begin(), keyInputs.end(), key) != keyInputs.end())
    {
        selectedKey = key;
        //cout << selectedKey << endl;
        
        // find the index of key on keyboard
        for (size_t i = 0; i < keyInputs.size(); i++)
        {
            if (keyInputs[i] == key)
                index = (int)i;
        }
        loadNote(notes[index], index);
    }
    
    selectedKey = -1;
}

//--------------------------------------------------------------
void testApp::mouseMoved(int x, int y ){
    
    if (y <= 0) {
        y = 0;
    }
    
    if (y >= ofGetHeight()) {
        y = ofGetHeight();
    }
	
    playbackLenght = (int)ofMap(y, 0, ofGetHeight(), 5.499, 1.499);
    cutoff = ofMap(y, 0, ofGetHeight(), 20000.0, 150.0);
    resonance = ofMap(y, 0, ofGetHeight(), 1.0, 4.0);
    delayTime = (int)ofMap(y, 0, ofGetHeight(), 1.499, 4.499);
}

//--------------------------------------------------------------
void testApp::mouseDragged(int x, int y, int button){
	
}

//--------------------------------------------------------------
void testApp::mousePressed(int x, int y, int button){
	
}

//--------------------------------------------------------------
void testApp::mouseReleased(int x, int y, int button){
	
}

//--------------------------------------------------------------
void testApp::windowResized(int w, int h){
	
}



//--------------------------------------------------------------
void testApp::gotMessage(ofMessage msg){

}

//--------------------------------------------------------------
void testApp::dragEvent(ofDragInfo dragInfo){ 

}