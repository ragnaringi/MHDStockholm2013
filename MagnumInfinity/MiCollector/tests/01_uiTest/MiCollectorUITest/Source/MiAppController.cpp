/*
  ==============================================================================

    MiAppController.cpp
    Created: 3 Apr 2013 9:40:29pm
    Author:  Owen Hindley

  ==============================================================================
*/

#include "../JuceLibraryCode/JuceHeader.h"
#include "MiAppController.h"


MiAppController::MiAppController() 
{
	printf("MiAppController :: called constructor");



}

MiAppController::~MiAppController()
{


}

void MiAppController::setup(DocumentWindow *document) {
    
    printf("MiAppController :: called constructor");
    
	parentDocument = document;

	uiManager = new MiUIManager();
	uiManager->setup(parentDocument);

}

void MiAppController::show(){
	uiManager->show();

}


void MiAppController::shutdown(){


}