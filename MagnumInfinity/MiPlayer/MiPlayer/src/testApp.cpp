#include "testApp.h"

//--------------------------------------------------------------
void testApp::setup(){
    
    
    ofEnableSmoothing();
	ofBackground(0);
	
	setGUI1();
    gui1->setDrawBack(false);

}

//--------------------------------------------------------------
void testApp::update(){

}

//--------------------------------------------------------------
void testApp::draw(){

    ofBackground(red, green, blue, 255); 
}

//--------------------------------------------------------------
void testApp::guiEvent(ofxUIEventArgs &e)
{
	string name = e.widget->getName();
	int kind = e.widget->getKind();
	cout << "got event from: " << name << endl;
	
	if(name == "RED")
	{
		ofxUISlider *slider = (ofxUISlider *) e.widget;
		cout << "RED " << slider->getScaledValue() << endl;
		red = slider->getScaledValue();
	}
	else if(name == "GREEN")
	{
		ofxUISlider *slider = (ofxUISlider *) e.widget;
		cout << "GREEN " << slider->getScaledValue() << endl;
		green = slider->getScaledValue();
	}
	
	else if(name == "BLUE")
	{
		ofxUISlider *slider = (ofxUISlider *) e.widget;
		cout << "BLUE " << slider->getScaledValue() << endl;
		blue = slider->getScaledValue();
	}
    else if(name == "TEXT INPUT")
    {
        ofxUITextInput *textinput = (ofxUITextInput *) e.widget;
        if(textinput->getTriggerType() == OFX_UI_TEXTINPUT_ON_ENTER)
        {
            cout << "ON ENTER: ";
            //            ofUnregisterKeyEvents((testApp*)this);
        }
        else if(textinput->getTriggerType() == OFX_UI_TEXTINPUT_ON_FOCUS)
        {
            cout << "ON FOCUS: ";
        }
        else if(textinput->getTriggerType() == OFX_UI_TEXTINPUT_ON_UNFOCUS)
        {
            cout << "ON BLUR: ";
            //            ofRegisterKeyEvents(this);
        }
        string output = textinput->getTextString();
        cout << output << endl;
    }
	
	
	
}
//--------------------------------------------------------------
void testApp::exit()
{
	delete gui1;
}

void testApp::setGUI1()
{
	red = 233; blue = 52; green = 27;
	
	float dim = 16;
	float xInit = OFX_UI_GLOBAL_WIDGET_SPACING;
    float length = 255-xInit;
	
    vector<string> names;
	names.push_back("RAD1");
	names.push_back("RAD2");
	names.push_back("RAD3");
	
	gui1 = new ofxUICanvas(0, 0, length+xInit, ofGetHeight());
	gui1->addWidgetDown(new ofxUILabel("PANEL 1: BASICS", OFX_UI_FONT_LARGE));
    gui1->addWidgetDown(new ofxUILabel("Press 'h' to Hide GUIs", OFX_UI_FONT_LARGE));
    
    gui1->addSpacer(length-xInit, 2);
	gui1->addWidgetDown(new ofxUILabel("H SLIDERS", OFX_UI_FONT_MEDIUM));
	gui1->addSlider("RED", 0.0, 255.0, red, length-xInit, dim);
	gui1->addSlider("GREEN", 0.0, 255.0, green, length-xInit,dim);
	gui1->addSlider("BLUE", 0.0, 255.0, blue, length-xInit,dim);
    
    gui1->addSpacer(length-xInit, 2);
    gui1->addWidgetDown(new ofxUILabel("V SLIDERS", OFX_UI_FONT_MEDIUM));
	gui1->addSlider("0", 0.0, 255.0, 150, dim, 160);
	gui1->setWidgetPosition(OFX_UI_WIDGET_POSITION_RIGHT);
	gui1->addSlider("1", 0.0, 255.0, 150, dim, 160);
	gui1->addSlider("2", 0.0, 255.0, 150, dim, 160);
	gui1->addSlider("3", 0.0, 255.0, 150, dim, 160);
	gui1->addSlider("4", 0.0, 255.0, 150, dim, 160);
	gui1->addSlider("5", 0.0, 255.0, 150, dim, 160);
	gui1->addSlider("6", 0.0, 255.0, 150, dim, 160);
	gui1->addSlider("7", 0.0, 255.0, 150, dim, 160);
	gui1->addSlider("8", 0.0, 255.0, 150, dim, 160);
	gui1->setWidgetPosition(OFX_UI_WIDGET_POSITION_DOWN);
    
    gui1->addSpacer(length-xInit, 2);
	gui1->addRadio("RADIO HORIZONTAL", names, OFX_UI_ORIENTATION_HORIZONTAL, dim, dim);
	gui1->addRadio("RADIO VERTICAL", names, OFX_UI_ORIENTATION_VERTICAL, dim, dim);
    
    gui1->addSpacer(length-xInit, 2);
	gui1->addWidgetDown(new ofxUILabel("BUTTONS", OFX_UI_FONT_MEDIUM));
	gui1->addButton("DRAW GRID", false, dim, dim);
	gui1->addWidgetDown(new ofxUILabel("TOGGLES", OFX_UI_FONT_MEDIUM));
	gui1->addToggle( "D_GRID", false, dim, dim);
    
    gui1->addSpacer(length-xInit, 2);
    gui1->addWidgetDown(new ofxUILabel("RANGE SLIDER", OFX_UI_FONT_MEDIUM));
	gui1->addRangeSlider("RSLIDER", 0.0, 255.0, 50.0, 100.0, length-xInit,dim);
    
    gui1->addSpacer(length-xInit, 2);
	gui1->addWidgetDown(new ofxUILabel("2D PAD", OFX_UI_FONT_MEDIUM));
	gui1->add2DPad("PAD", ofPoint(0,length-xInit), ofPoint(0,120), ofPoint((length-xInit)*.5,120*.5), length-xInit,120);
    

	ofAddListener(gui1->newGUIEvent,this,&testApp::guiEvent);
}


//--------------------------------------------------------------
void testApp::keyPressed(int key){

}

//--------------------------------------------------------------
void testApp::keyReleased(int key){

}

//--------------------------------------------------------------
void testApp::mouseMoved(int x, int y ){

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