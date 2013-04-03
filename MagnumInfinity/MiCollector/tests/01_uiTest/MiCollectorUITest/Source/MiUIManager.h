/*
  ==============================================================================

    MiUIManager.h
    Created: 3 Apr 2013 10:02:38pm
    Author:  Owen Hindley

  ==============================================================================
*/

#ifndef __MIUIMANAGER_H_C52AA966__
#define __MIUIMANAGER_H_C52AA966__

#include "../JuceLibraryCode/JuceHeader.h"

class MiUIManager
{
public:

	MiUIManager();
	~MiUIManager();

	void setup(DocumentWindow *document);
	void show();

private:

	DocumentWindow *parentDocument;
	Image *backgroundImage;

};

#endif  // __MIUIMANAGER_H_C52AA966__
