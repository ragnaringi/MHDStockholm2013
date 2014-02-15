(function() {
	

	window.miKeyboardController = function() {

		this._keys = {};
		this._sampleManager = null;
	};

	var p = window.miKeyboardController.prototype;

	p.setup = function(aContainer, aSampleManager) {

		this._sampleManager = aSampleManager;

		var keyElements = aContainer.querySelectorAll(".note");

		for (var i=0; i< keyElements.length; i++){

			var noteElement = keyElements[i];
			var noteName = noteElement.getAttribute("id").split("note")[1];
			this._keys[noteName] = noteElement;
			noteElement.addEventListener("mousedown", function(aEvent){
				var noteName = aEvent.target.getAttribute("id").split("note")[1];
				this.playNote(noteName);
			}.bind(this));

			noteElement.addEventListener("mouseup", function(aEvent){
				var noteName = aEvent.target.getAttribute("id").split("note")[1];
				this.stopNote(noteName);
			}.bind(this));


		}

		document.addEventListener("keydown", function(aEvent){

			var keyName = String.fromCharCode(aEvent.keyCode).toLowerCase();

			switch(keyName){
				case "a":
					this.playNote("C");
				break;
				case "w":
					this.playNote("Db");
				break;
				case "s":
					this.playNote("D");
				break;
				case "e":
					this.playNote("Eb");
				break;
				case "d":
					this.playNote("E");
				break;
				case "f":
					this.playNote("F");
				break;
				case "t":
					this.playNote("Gb");
				break;
				case "g":
					this.playNote("G");
				break;
				case "y":
					this.playNote("Ab");
				break;
				case "h":
					this.playNote("A");
				break;
				case "u":
					this.playNote("Bb");
				break;
				case "j":
					this.playNote("B");
				break;

			}


		}.bind(this));


		document.addEventListener("keyup", function(aEvent){

			var keyName = String.fromCharCode(aEvent.keyCode).toLowerCase();

			switch(keyName){
				case "a":
					this.stopNote("C");
				break;
				case "w":
					this.stopNote("Db");
				break;
				case "s":
					this.stopNote("D");
				break;
				case "e":
					this.stopNote("Eb");
				break;
				case "d":
					this.stopNote("E");
				break;
				case "f":
					this.stopNote("F");
				break;
				case "t":
					this.stopNote("Gb");
				break;
				case "g":
					this.stopNote("G");
				break;
				case "y":
					this.stopNote("Ab");
				break;
				case "h":
					this.stopNote("A");
				break;
				case "u":
					this.stopNote("Bb");
				break;
				case "j":
					this.stopNote("B");
				break;

			}


		}.bind(this));

	};

	p.playNote = function(aNoteName){
		this._sampleManager.playNote(aNoteName);
	}

	p.stopNote = function(aNoteName){
		this._sampleManager.stopNote(aNoteName);
	}



})();