#include "testApp.h"

// This data will be used to make a volume envelope. Value and time to value in ms.
double attackEnvData[4] = {0,0,1,150};
double decayEnvData[4] =  {1,0,0,150};

// Allowed key values
#define NUM_NOTES 11
static const int keyValues[NUM_NOTES] = {97,115,100,102,103,104,106,107,108,59,39};
static const string notes[NUM_NOTES] = {"A", "Bb", "B", "C", "Db", "Eb", "E", "F", "Gb", "G", "Ab"};

//-------------------------------------------------------------
testApp::~testApp() {
	
    for (int i = 0; i < NUM_NOTES; i++) {
        sample[i].clear();
    }
}

//--------------------------------------------------------------
void testApp::setup(){
    
    ofTrueTypeFont::setGlobalDpi(72);
    font.loadFont("GUI/NewMedia Fett.ttf", 52, true, true); //open source font
	
    /* Sample directories are placed in Data folder */
    ofDirectory patchDir(ofToDataPath("SAMPLES", false));
    patchDir.allowExt("");
    int numPatches = patchDir.listDir();
    if (numPatches > 0) {
        for (int i = 0; i < numPatches; i++) {
            cout << "Synth patches: " << patchDir.getFiles()[i].getFileName() << endl;
        }
        synthpatch = "SAMPLES/" + patchDir.getFiles()[0].getFileName();
    }
    else {
        ofLog(OF_LOG_ERROR, "NO SYNTH PATCH FOUND");
    }
    
    cout << "Current synthpatch: " << synthpatch << endl;
    
    loadSynthPatch();
    
    envelope.trigger(0, decayEnvData[0]);
    playbackLength = 1;
    cutoff = 0.9;
    
	ofSoundStreamSetup(2,0,this, 44100, 1024, 4);/* Call this last ! */
}

//--------------------------------------------------------------
void testApp::update(){
	
}

//--------------------------------------------------------------
void testApp::draw(){
	
    ofBackground(0, 0, 0);
	ofSetColor(255, 255, 255);
    
    ofDrawBitmapString("Play buttons [ A ] through to [ ' ] on your keyboard", 20.f, 20.f);
    
    string playingNote = "Playing Note:";
    font.drawString(playingNote, ofGetWidth()/2 - (font.stringWidth(playingNote) * .5), int(ofGetHeight()/2.5));
    
    string noteSymbol = notePlaying;
    font.drawString(noteSymbol, ofGetWidth()/2 - (font.stringWidth(noteSymbol) * .5), int(ofGetHeight()/2));
}

//--------------------------------------------------------------
void testApp::audioRequested(float * output, int bufferSize, int nChannels){
	
	for (int i = 0; i < bufferSize; i++){
        
        if (currentSample == NULL) return;
        
        // Playback
        leftOutput = currentSample->play(1.0, 0, currentSample->length); // mono only
        
        // Loop length
        if (currentSample->position >= (currentSample->length/(double)playbackLength) - 1) {
            currentSample->position = 0;
        }
        
        // Filter
        leftOutput = filter.lores(leftOutput, cutoff, 4.0);
        
        // Amplitude
        if (shouldPlay) {
            outVolume = envelope.line(4, attackEnvData);
        }
        else {
            outVolume = envelope.line(4, decayEnvData);
        }
        leftOutput *= outVolume;
        
        // Output
		mainMix.stereo(leftOutput, outputs, 0.5);
		
		output[i*nChannels    ] = outputs[0]; /* You may end up with lots of outputs. add them here */
		output[i*nChannels + 1] = outputs[1];
	}
	
}

//--------------------------------------------------------------
void testApp::audioReceived(float * input, int bufferSize, int nChannels){
	
	/* You can just grab this input and stick it in a double, then use it above to create output*/
	
	for (int i = 0; i < bufferSize; i++){
		
		/* you can also grab the data out of the arrays*/
	}
}


//--------------------------------------------------------------
void testApp::keyPressed(int key){
    
    int index = -1;
    
    if (selectedKey == key) return;
    
    // find the index of key on keyboard
    for (int i = 0; i < NUM_NOTES; i++)
    {
        if (keyValues[i] == key) {
            selectedKey = key;
            index = i;
            break;
        }
    }
    
    if (index == -1) return;
    
    shouldPlay = true;
    envelope.trigger(0, attackEnvData[0]);
    playNote(notes[index], index);
    
    notePlaying = notes[index];
}

//--------------------------------------------------------------
void testApp::keyReleased(int key){
    
    int index = -1;
    
    // find the index of key on keyboard
    for (int i = 0; i < NUM_NOTES; i++)
    {
        if (keyValues[i] == key) {
            index = i;
            break;
        }
    }
    if  (index == -1) return;
    
    double delayMS = 0.0;
    
    if  (key == selectedKey) {
        shouldPlay = false;
        envelope.trigger(0, decayEnvData[0]);
        delayMS = decayEnvData[3] + 20.0;
        selectedKey = -1;
    }
    
    // Delay loading next sample until note has faded
    dispatch_time_t delay = dispatch_time(DISPATCH_TIME_NOW, delayMS * NSEC_PER_MSEC);
    dispatch_after(delay, dispatch_get_main_queue(), ^{
        loadNote(notes[index], index);
    });
    
    notePlaying = "";
}

//--------------------------------------------------------------
void testApp::mouseMoved(int x, int y ){
    
    if (y <= 0) {
        y = 0;
    }
    
    if (y >= ofGetHeight()) {
        y = ofGetHeight();
    }
	
    playbackLength = (int)ofMap(y, 0, ofGetHeight(), 5.499, 1.499);
    cutoff = ofMap(y, 0, ofGetHeight(), 20000.0, 150.0);
}

//--------------------------------------------------------------
void testApp::playNote(string key, int index) {
    
    sample[index].getLength();
    if (sample[index].myDataSize == 0) return;
    currentSample = &sample[index];
}

//--------------------------------------------------------------
void testApp::loadNote(string key, int index) {
    
    // When key is released, load next available sample
    // for this note
    
    string path = ofToDataPath(synthpatch);
    path += "/" + key;

    ofDirectory dir(path);
    if (dir.exists()) {
        dir.allowExt("wav");
        dir.listDir();
        vector<ofFile>samplePaths = dir.getFiles();
        // find the index of current sample in this directory
        int sampleNumber = 0;

        for (int i = 0; i < samplePaths.size(); i++)
        {
            if (currentSamplePaths[index] == samplePaths[i].path()) {
                sampleNumber = i;
            }
        }
        sampleNumber++;
        if (sampleNumber >= samplePaths.size() - 1) {
            sampleNumber = 0;
        }
        
        string pathToLoad = samplePaths[sampleNumber].path();
        sample[index].load(pathToLoad);
        
        currentSamplePaths[index] = pathToLoad;
    }
}

//--------------------------------------------------------------
void testApp::loadSynthPatch() {
    
    for (int i = 0; i < NUM_NOTES; i++) {
        string path = ofToDataPath(synthpatch) += "/" + notes[i];
        ofDirectory dir(path);
        if (dir.exists()) {
            dir.allowExt("wav");
            dir.listDir();
            
            string pathToLoad = dir.getFiles()[0].path();
            currentSamplePaths[i] = pathToLoad;
            
            sample[i].load(pathToLoad);
            sample[i].getLength();
            currentSample = &sample[0];
        }
    }
}
