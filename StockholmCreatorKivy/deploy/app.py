import kivy
kivy.require('1.8.0') # replace with your current kivy version !

from os.path import sep, expanduser, isdir, dirname

from classes.StockholmAudioAnalyser import StockholmAudioAnalyser, SampleReference

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from libs.filebrowser_class import FileBrowser

from kivy.logger import Logger

from kivy.config import Config

Config.set('kivy', 'log_name', 'log.txt')

class MyApp(App):



	def sourceFolderSelectCallback(self, instance):

		Logger.info("selected :")
		# Logger.info(instance.selection)
		# Logger.info(instance.path)

		self.sourceFolder = instance.path

		self.sourceFolderLabel.text = self.sourceFolder

		self.layout.remove_widget(self.fileBrowser)

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

	def onSelectDestinationFolderClick(self, instance):

		user_path = expanduser('~') + sep + 'Documents'
		self.fileBrowser = FileBrowser(select_string='Select', multiselect=True, favorites=[(user_path, 'Documents')])
		self.fileBrowser.bind(on_success=self.destFolderSelectCallback)
		
		self.layout.add_widget(self.fileBrowser)


	def doAnalysis(self, instance):

		self.analyser = StockholmAudioAnalyser(self.sourceFolder, self.destFolder, 0.2, 0.6, 1)
		self.analyser.analyseFiles()
		self.analyser.sortSimilarSamples()
		self.analyser.exportFiles()

	def showAnalyseButton(self):

		self.analyseButton = Button(text="Get Notes", font_size=14, size_hint=(0.2, 0.2), pos_hint={'x' : .4, 'y' : .2})
		self.analyseButton.bind(on_press=self.doAnalysis)

		self.layout.add_widget(self.analyseButton)

	def build(self):

		self.layout = FloatLayout()

		self.audioAnalyser = None

		self.selectSourceButton = Button(text="Select Source Folder", font_size=14, size_hint=(0.1, 0.1), pos_hint={'x' : .2, 'y' : .2})
		self.selectSourceButton.bind(on_press=self.onSelectSourceFolderClick)

		self.selectDestinationButton = Button(text="Select Destination Folder", font_size=14, size_hint=(0.1, 0.1), pos_hint={'x' : .2, 'y' : .6})
		self.selectDestinationButton.bind(on_press=self.onSelectDestinationFolderClick)

		self.sourceFolderLabel = Label(text="No Source Folder Set", font_size=14, size_hint=(0.2, 0.1), pos_hint={'x' : .2, 'y' : .3})
		self.destinationFolderLabel = Label(text="No Destination Folder Set", font_size=14, size_hint=(0.1, 0.1), pos_hint={'x' : .2, 'y' : .1})

		self.layout.add_widget(self.selectSourceButton)
		self.layout.add_widget(self.selectDestinationButton)
		self.layout.add_widget(self.sourceFolderLabel)
		self.layout.add_widget(self.destinationFolderLabel)

		# self.layout.add_widget(self.createFileBrowser())

		return self.layout

if __name__ == '__main__':
	MyApp().run()
    