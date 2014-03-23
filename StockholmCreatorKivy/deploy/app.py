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

class LoadDialog(Popup):

    def load(self, path, selection):
        self.choosen_file = [None, ]
        self.choosen_file = selection
        Window.title = selection[0][selection[0].rfind(os.sep)+1:]
        self.dismiss()

    def cancel(self):
        self.dismiss()



class MyApp(App):



	def sourceFolderSelectCallback(self):

		print("Opened filebrowser successfully")

	def destFolderSelectCallback(self):

		print("Opened filebrowser successfully")
	

	def onSelectSourceFolderClick(self, instance):

		user_path = expanduser('~') + sep + 'Documents'
		self.fileBrowser = FileBrowser(select_string='Select', favorites=[(user_path, 'Documents')])
		self.fileBrowser.bind(on_success=self.sourceFolderSelectCallback)
		self.layout.add_widget(self.fileBrowser)

	def onSelectDestinationFolderClick(self, instance):

		user_path = expanduser('~') + sep + 'Documents'
		self.fileBrowser = FileBrowser(select_string='Select', favorites=[(user_path, 'Documents')])
		self.fileBrowser.bind(on_success=self.destFolderSelectCallback)
		
		self.layout.add_widget(self.fileBrowser)


	def doAnalysis(self, instance):

		self.analyser = StockholmAudioAnalyser("./testSamples", "./outputSamples", 0.2, 0.6, 1)
		self.analyser.analyseFiles()
		self.analyser.sortSimilarSamples()
		self.analyser.exportFiles()


	def build(self):

		self.layout = FloatLayout()

		self.audioAnalyser = None

		self.selectSourceButton = Button(text="Select Source Folder", font_size=14, size_hint=(0.2, 0.2), pos_hint={'x' : .2, 'y' : .2})
		self.selectSourceButton.bind(on_press=self.onSelectSourceFolderClick)

		self.selectDestinationButton = Button(text="Select Destiation Folder", font_size=14, size_hint=(0.2, 0.2), pos_hint={'x' : .2, 'y' : .6})
		self.selectDestinationButton.bind(on_press=self.onSelectDestinationFolderClick)



		self.layout.add_widget(self.selectSourceButton)
		self.layout.add_widget(self.selectDestinationButton)

		# self.layout.add_widget(self.createFileBrowser())

		return self.layout

if __name__ == '__main__':
	MyApp().run()
    