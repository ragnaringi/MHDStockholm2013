(function() {
	

	window.miSample = function() {

		this._loadedCallback = null;

		this._fileObject = null;

		this._reader = null;
		this._context = null;
		this._soundBuffer = null;
		this._soundSource = null;
		this._gainNode = null;
	};

	var p = window.miSample.prototype;

	p.setup = function(aFileObject, aContext) {

		this._context = aContext;

		this._reader = new FileReader();
		this._reader.onload = this._fileLoaded.bind(this);

		this._fileObject = aFileObject;

	};

	p.load = function(aCallback){
		this._loadedCallback = aCallback;
		this._reader.readAsArrayBuffer(this._fileObject);
	}

	p._fileLoaded = function(aEvent) {

		console.log(this._fileObject.name, "loaded");

		this._context.decodeAudioData(aEvent.target.result, this._decodeCompleted.bind(this));

	};

	p._decodeCompleted = function(rawBuffer){

		this._soundBuffer = rawBuffer;

		this._gainNode = this._context.createGain();
		this._gainNode.gain.value = 0;
		this._gainNode.connect(this._context.destination);

		console.log(this._fileObject.name, "decoded");
		this._loadedCallback.call(this);

	};

	p.play = function(aNextCallback){

		this._soundSource = this._context.createBufferSource();
		this._soundSource.buffer = this._soundBuffer;
		this._soundSource.connect(this._gainNode);

		this._soundSource.start(this._context.currentTime);

		this._fadeIn();

		setTimeout(function() {
			this._fadeOut();
			aNextCallback.call(this);	
		}.bind(this), Math.floor(this._soundBuffer.duration * 0.8 * 1000));

	};

	p._fadeIn = function() {

		var fadeTime = this._soundBuffer.duration * 0.2 * 1000;
		var gain = this._gainNode.gain;
		var fadingTween = new TWEEN.Tween({ gainEnvelope : 0}).to({ gainEnvelope : 1}, fadeTime).onUpdate(function() {
			gain.value = this.gainEnvelope;
		}).start();

	}

	p._fadeOut = function(){

		var fadeTime = this._soundBuffer.duration * 0.2 * 1000;
		var gain = this._gainNode.gain;
		var fadingTween = new TWEEN.Tween({ gainEnvelope : 1}).to({ gainEnvelope : 0}, fadeTime).onUpdate(function() {
			gain.value = this.gainEnvelope;
		}).start();

	};



})();