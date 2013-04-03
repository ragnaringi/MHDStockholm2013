/*
  ==============================================================================

    MiAppController.h
    Created: 3 Apr 2013 9:40:29pm
    Author:  Owen Hindley

  ==============================================================================
*/

#ifndef __MIAPPCONTROLLER_H_22138CEA__
#define __MIAPPCONTROLLER_H_22138CEA__

#include "../JuceLibraryCode/JuceHeader.h"

#include "MiUIManager.h"

class MiAppController
{
public:

	MiAppController();
	~MiAppController();

	void setup(DocumentWindow *document);
	void show();
	void shutdown();

private:

	DocumentWindow *parentDocument;
	MiUIManager *uiManager;

};

#endif  // __MIAPPCONTROLLER_H_22138CEA__
