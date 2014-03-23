import kivy
kivy.require('1.8.0') # replace with your current kivy version !

from os.path import sep, expanduser, isdir, dirname

from classes.StockholmAudioAnalyser import StockholmAudioAnalyser, SampleReference

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from libs.filebrowser_class import FileBrowser

from kivy.logger import Logger

from kivy.config import Config

import thread

Config.set('kivy', 'log_name', 'log.txt')

class MyApp(App):



	def sourceFolderSelectCallback(self, instance):

		Logger.info("selected :")
		# Logger.info(instance.selection)
		# Logger.info(instance.path)

		self.sourceFolder = instance.path

		self.sourceFolderLabel.text = self.sourceFolder

		self.layout.remove_widget(self.fileBrowser)

		self.layout.add_widget(self.buttonContainer)

		try:
			self.destFolder
			self.showAnalyseButton()
		except:
			Logger.info("Waiting for destination folder to be set")
		
			

	def destFolderSelectCallback(self, instance):

		Logger.info("selected :")
		# Logger.info(instance.selection)
		# Logger.info(instance.path)

		self.destFolder = instance.path

		self.destinationFolderLabel.text = self.destFolder

		self.layout.remove_widget(self.fileBrowser)

		self.layout.add_widget(self.buttonContainer)


		try:
			self.sourceFolder
			self.showAnalyseButton()
		except:
			Logger.info("Waiting for source folder to be set")
	

	def onSelectSourceFolderClick(self, instance):

		user_path = expanduser('~') + sep + 'Documents'
		self.fileBrowser = FileBrowser(select_string='Select', multiselect=True, favorites=[(user_path, 'Documents')])
		self.fileBrowser.bind(on_success=self.sourceFolderSelectCallback)
		self.layout.add_widget(self.fileBrowser)

		self.layout.remove_widget(self.buttonContainer);

	def onSelectDestinationFolderClick(self, instance):

		user_path = expanduser('~') + sep + 'Documents'
		self.fileBrowser = FileBrowser(select_string='Select', multiselect=True, favorites=[(user_path, 'Documents')])
		self.fileBrowser.bind(on_success=self.destFolderSelectCallback)
		
		self.layout.add_widget(self.fileBrowser)
		self.layout.remove_widget(self.buttonContainer);


	def startAnalysis(self, instance):

		self.layout.remove_widget(self.buttonContainer);

		self.consoleOutput = ScreenLogger()
		self.layout.add_widget(self.consoleOutput.widget)

		self.analyser = StockholmAudioAnalyser(self.sourceFolder, self.destFolder, self.minAvgSlider.value, self.minDurationSlider.value, self.maxDurationSlider.value)
		self.analyser.setConsoleOutput(self.consoleOutput)

		thread.start_new_thread(self.doAnalysis, ())
		

	def doAnalysis(self):
		self.analyser.analyseFiles()
		self.analyser.sortSimilarSamples()
		self.analyser.exportFiles()

		self.consoleOutput.write("*************************")
		self.consoleOutput.write("Sample analysis complete.")
		self.consoleOutput.write("Please check your output folder")

		self.layout.remove_widget(self.consoleOutput.widget)

		completeLabel = Label(text="**********************\nSample Analysis Complete\nPlease check your output folder", font_size=24, width=800, size_hint=(None, 0.3), pos=(0,0))
		self.layout.add_widget(completeLabel)


	def showAnalyseButton(self):

		self.analyseButton = Button(text="Get Notes", font_size=14, width=600, size_hint=(None, 0.15))
		self.analyseButton.bind(on_press=self.startAnalysis)

		self.buttonContainer.add_widget(self.analyseButton)

	def build(self):

		self.title = 'Stockholm Sample Creator'

		self.layout = FloatLayout()

		self.buttonContainer = StackLayout(pos=(10,10), size_hint=(.9, .9))

		self.audioAnalyser = None

		headerLabel = Label(text="Stockholm Sample Creator", halign="left", font_size=24, width=800, size_hint=(None, 0.3), pos=(0,0))
		self.buttonContainer.add_widget(headerLabel)

		self.selectSourceButton = Button(text="Select Source Folder", font_size=14,  width=300, size_hint=(None, 0.1))
		self.selectSourceButton.bind(on_press=self.onSelectSourceFolderClick)

		self.selectDestinationButton = Button(text="Select Destination Folder", font_size=14, width=300, size_hint=(None, 0.1))
		self.selectDestinationButton.bind(on_press=self.onSelectDestinationFolderClick)

		self.sourceFolderLabel = Label(text="No Source Folder Set", font_size=14, width=300, size_hint=(None, 0.1))
		self.destinationFolderLabel = Label(text="No Destination Folder Set", font_size=14, width=300, size_hint=(None, 0.1))

		self.buttonContainer.add_widget(self.selectSourceButton)
		self.buttonContainer.add_widget(self.selectDestinationButton)
		self.buttonContainer.add_widget(self.sourceFolderLabel)
		self.buttonContainer.add_widget(self.destinationFolderLabel)

		sliderLabel = Label(text='Minimum pitch deviation (lower=more accurate, fewer samples)', font_size=10, width=200, size_hint=(None, 0.1))
		self.minAvgSlider = Slider(min=0, max=0.99, value=0.2, padding=50, width=400, size_hint=(None, 0.1))

		minDurationSliderLabel = Label(text='Minimum note duration', font_size=10, width=200, size_hint=(None, 0.1))
		self.minDurationSlider = Slider(min=0, max=2, value=0.2, padding=50, width=400, size_hint=(None, 0.1))

		maxDurationSliderLabel = Label(text='Maximum note duration', font_size=10, width=200, size_hint=(None, 0.1))
		self.maxDurationSlider = Slider(min=0, max=2, value=1, padding=50, width=400, size_hint=(None, 0.1))

		
		self.buttonContainer.add_widget(self.minAvgSlider)
		self.buttonContainer.add_widget(sliderLabel)

		self.buttonContainer.add_widget(self.minDurationSlider)
		self.buttonContainer.add_widget(minDurationSliderLabel)

		self.buttonContainer.add_widget(self.maxDurationSlider)
		self.buttonContainer.add_widget(maxDurationSliderLabel)

		self.layout.add_widget(self.buttonContainer)

		# DEBUG
		# self.sourceFolder = "/Users/owenhindley/Desktop/test-samples"
		# self.destFolder = "/Users/owenhindley/Desktop/test-output"

		# self.showAnalyseButton()

		# self.layout.add_widget(self.createFileBrowser())

		return self.layout

class ScreenLogger:

	def __init__(self):
		self.widget = Label(text="", font_size=12, width=800, size_hint=(None, 1))

	def write(self, aMessage):
		Logger.info(aMessage)
		self.widget.text += aMessage + "\n"

if __name__ == '__main__':
	MyApp().run()
    