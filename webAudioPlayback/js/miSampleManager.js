(function() {
	

	window.miSampleManager = function() {

		this._noteSamples = {};
		this._sampleLoadQueue = [];
		this._patchTitle = "";

		this._completeCallback = null;

		this._currentlyPlayingNotes = {};

		this._context = null;

	};

	var p = window.miSampleManager.prototype;

	p.setup = function(aSampleList, aCallback) {

		this._context = new webkitAudioContext();

		this._completeCallback = aCallback;

		console.log("miSampleManager :: received file list, ", aSampleList.length, " samples");

		var title = "";
		var rawFile, pathComponents, noteName, groupName, filenameComponents;

		for (var i=0; i< aSampleList.length; i++){

			rawFile = aSampleList[i];

			if (rawFile.name.indexOf(".wav") != -1){

				pathComponents = rawFile.webkitRelativePath.split("/");
				title = pathComponents[0];
				noteName = pathComponents[1];
				filenameComponents = pathComponents[2].split("_");
				groupName = filenameComponents[1];
				groupName = 0;

				if (!this._noteSamples[noteName]) this._noteSamples[noteName] = {};
				if (!this._noteSamples[noteName][groupName]) this._noteSamples[noteName][groupName] = [];

				var newSample = new miSample();
				newSample.setup(rawFile, this._context);

				this._noteSamples[noteName][groupName].push(newSample);
				this._sampleLoadQueue.push(newSample);

			}


		}

		this._loadNextSample();

	};

	p._loadNextSample = function() {
		if (this._sampleLoadQueue.length){
			this._sampleLoadQueue.pop().load(this._loadNextSample.bind(this));
		} else {
			console.log("loading complete");
			this._completeCallback.call(this);
		}
	};


	p.playNote = function(aNoteName) {

		if (!this._currentlyPlayingNotes[aNoteName]){

			this._currentlyPlayingNotes[aNoteName] = {
				samples : [],
				sampleIndex : -1,
				nextSampleIntervalId : -1
			};

			var playbackObj = this._currentlyPlayingNotes[aNoteName];
			playbackObj.samples = this._noteSamples[aNoteName][0];

			this._playNextSample(aNoteName);

		}

	};

	p._playNextSample = function(aNoteName){

		if (this._currentlyPlayingNotes[aNoteName]) {
			var playbackObj = this._currentlyPlayingNotes[aNoteName];
			playbackObj.sampleIndex++;
			if (playbackObj.sampleIndex >= playbackObj.samples.length) playbackObj.sampleIndex = 0;
			console.log("playing note ", aNoteName, " sample index ", playbackObj.sampleIndex);
			playbackObj.samples[playbackObj.sampleIndex].play(function() {
				this._playNextSample(aNoteName);
			}.bind(this));
		}

	};


	p.stopNote = function(aNoteName) {

		this._currentlyPlayingNotes[aNoteName] = null;

	};



})();