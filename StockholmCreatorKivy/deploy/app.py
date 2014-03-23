import kivy
kivy.require('1.8.0') # replace with your current kivy version !


from classes.StockholmAudioAnalyser import StockholmAudioAnalyser, SampleReference

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup

class LoadDialog(Popup):

    def load(self, path, selection):
        self.choosen_file = [None, ]
        self.choosen_file = selection
        Window.title = selection[0][selection[0].rfind(os.sep)+1:]
        self.dismiss()

    def cancel(self):
        self.dismiss()



class MyApp(App):

    def build(self):

    	self.layout = GridLayout(cols=5,rows=5)

    	self.audioAnalyser = None

    	self.goButton = Button(text="Go!", font_size=14)
    	
    	self.goButton.bind(on_press=self.doAnalysis)

    	self.layout.add_widget(self.goButton)
    
        return self.layout

    def doAnalysis(self, instance):

		self.analyser = StockholmAudioAnalyser("./testSamples", "./outputSamples", 0.2, 0.6, 1)
		self.analyser.analyseFiles()
		self.analyser.sortSimilarSamples()
		self.analyser.exportFiles()




if __name__ == '__main__':
    MyApp().run()