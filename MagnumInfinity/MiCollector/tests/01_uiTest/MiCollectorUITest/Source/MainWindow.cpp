/*
  ==============================================================================

    This file was auto-generated!

    It contains the basic outline for a simple desktop window.

  ==============================================================================
*/

#include "MainWindow.h"


//==============================================================================
MainAppWindow::MainAppWindow()
    : DocumentWindow ("Magnum Infinity :: UI Test",
                      Colours::white,
                      DocumentWindow::allButtons)
{

    appController = new MiAppController();

    centreWithSize (800, 400);
    setVisible (true);

    appController->setup(this);
    appController->show();

}

MainAppWindow::~MainAppWindow()
{
    
}

void MainAppWindow::closeButtonPressed()
{
    appController->shutdown();
    JUCEApplication::getInstance()->systemRequestedQuit();
}
