(function() {
	


	window.miPlaybackTest = function() {

		this._fileSelector = null;

		this._rawSamples = [];

		this._sampleManager = null;

		this._keyboardManager = null;

	};

	var p = window.miPlaybackTest.prototype;

	p.setup = function() {

		this._fileSelector = document.getElementById("file_input");
		this._fileSelector.onchange = this._onFilesSelected.bind(this);

		this._sampleManager = new miSampleManager();

	};

	p._onFilesSelected = function(aEvent){
		
		document.getElementById("inputSelector").style.display = "none";
		document.getElementById("loadingMessageContainer").style.display = "block";

		document.getElementById("loadingMessage").innerHTML = "Loading " + aEvent.target.files.length + " samples...";


		this._sampleManager.setup(aEvent.target.files, this._onSamplesLoaded.bind(this));

	};

	p._onSamplesLoaded = function() {

		document.getElementById("loadingMessageContainer").style.display = "none";
		document.getElementById("playback").style.display = "block";

		this._keyboardManager = new miKeyboardController();
		this._keyboardManager.setup(document.getElementById("keyboard"), this._sampleManager);

	};


})();