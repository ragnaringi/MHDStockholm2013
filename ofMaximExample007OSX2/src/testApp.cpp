/* This is an example of how to integrate maximilain into openFrameworks, 
 including using audio received for input and audio requested for output.
 
 
 You can copy and paste this and use it as a starting example.
 
 */


#include "testApp.h"


double myEnvelopeData[8] = {0,0,1,500,1,500,0,500};//this data will be used to make an envelope. Value and time to value in ms.

// Vector with allowed key values
static const int keys[12] = {97,115,100,102,103,104,106,107,108,59,39,92};
vector<int> vec (keys, keys + sizeof(keys) / sizeof(keys[0]) );


//-------------------------------------------------------------
testApp::~testApp() {
	
	delete sample.myData; /*you should probably delete myData for any sample object
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
	initialBufferSize	= 512;	/* Buffer Size. you have to fill this buffer with sound*/
	
	/* Now you can put anything you would normally put in maximilian's 'setup' method in here. */
	
    //some path, may be absolute or relative to bin/data
    string path = ofToDataPath("");
    ofDirectory dir(path);
    //only show wav files
    dir.allowExt("wav");
    //populate the directory object
    dir.listDir();
    samplePaths = dir.getFiles();
    
    sampleNumber = 0;
	
    playSample = false;
    
    myEnvelope.amplitude=myEnvelopeData[0]; //initialise the envelope
    
    cutoff = 0.9;
    delayTime = 1;
    
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
            leftOutput = sample.play(1.0, 0, sample.length);
        }
        
        if (sample.position >= sample.length - 1) {
            sampleNumber++ ;
            
            sample.load(samplePaths[sampleNumber].path());
            sample.getLength();
            
            //Attack time
            myEnvelopeData[3] = (double)(sample.length/16) / 44.1;
            //Sustain time
            myEnvelopeData[5] = (sample.length/2) / 44.1;
            //Release time
            myEnvelopeData[7] = (sample.length/16) / 44.1;
            
            if (sampleNumber >= samplePaths.size() - 1) {
                sampleNumber = 0;
            }
            
            myEnvelope.trigger(0,myEnvelopeData[0]);
            
            playSample = true;
        }
        
        leftOutput = myFilter.lores(leftOutput, cutoff, 4.0);
        leftOutput *= outVolume;
        
        double delayOut = delay.dl(leftOutput, sample.length/delayTime, 0.9);
        
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

//--------------------------------------------------------------
void testApp::keyPressed(int key){
    
    int selected;
	if (std::find(vec.begin(), vec.end(), key) != vec.end())
    {
        selected = key;
        cout << "key: " << selected << endl;
    }
}

//--------------------------------------------------------------
void testApp::keyReleased(int key){
	
}

//--------------------------------------------------------------
void testApp::mouseMoved(int x, int y ){
	
    cutoff = ofMap(y, 0, ofGetHeight(), 20000.0, 150.0);
    resonance = ofMap(y, 0, ofGetHeight(), 1.0, 4.0);
    delayTime = (int)ofMap(y, 0, ofGetHeight(), 1.0, 10.0);
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