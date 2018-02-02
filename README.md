# Aurora Python SDK


## Overview

Aurora is the enterprise end-to-end speech solution. This Python SDK will allow you to quickly and easily use the Aurora service to integrate voice capabilities into your application.

The SDK is currently in a pre-alpha release phase. Bugs and limited functionality should be expected.

## Installation

**The Recommended Python version is 3.0+**

The Python SDK currently does not bundle the necessary system headers and binaries to interact with audio hardware in a cross-platform manner. For this reason, before using the SDK, you need to install `PortAudio`:

### macOS

```
$ brew install portaudio
$ pip install pyaudio
$ pip install auroraapi
```

Note that you may need to use `pip2` if you are using `python2` or `pip3` if you are using `python3`.

### Linux

```
$ sudo apt-get install python-pyaudio
$ pip install auroraapi
```

This will install `PyAudio` as well as its dependencies (`PortAudio`). Use `yum` if your distribution uses `RPM`-based packages. If your distribution does not have `PortAudio` in its repository, install [PortAudio via source](http://www.portaudio.com/download.html) and then install `pyaudio` using `pip`.


## Basic Usage

First, make sure you have an account with [Aurora](http://dashboard.auroraapi.com) and have created an Application.

### Text to Speech (TTS)

```python
# Import the package
import auroraapi as aurora

# Set your application settings
aurora.set_app_id("YOUR_APP_ID")       # put your app ID here
aurora.set_app_token("YOUR_APP_TOKEN") # put your app token here

# query the TTS service
speech = aurora.Text("Hello world").speech()

# play the resulting audio
speech.audio.play()

# or save it to a file
speech.audio.write_to_file("test.wav")
```

### Speech to Text (STT)

#### Convert a WAV file to Speech

```python
# Import the package
import auroraapi as aurora

# Set your application settings
aurora.set_app_id("YOUR_APP_ID")       # put your app ID here
aurora.set_app_token("YOUR_APP_TOKEN") # put your app token here

# load a WAV file
a = aurora.audio.AudioFile.create_from_filename("test.wav")

# or open an already-open file
# with open("test.wav", "rb") as f:
#   a = aurora.audio.AudioFile.create_from_file(f)

p = aurora.Speech(a).text()
print(p.text) # 'hello world'
```

#### Convert a previous Text API call to Speech
```python
# Call the TTS API to convert "Hello world" to speech
speech = aurora.Text("Hello world").speech()

# Previous API returned a Speech object, so we can just call
# the text() method to get a prediction
p = speech.text()
print(p.text) # 'hello world'
```

#### Listen for a specified amount of time
```python
# Listen for 3 seconds (silence is automatically trimmed)
speech = aurora.Speech.listen(length=3)

# Convert to text
p = speech.text()
print(p.text) # prints the prediction
```

#### Listen for an unspecified amount of time

Calling this API will start listening and will automatically stop listening after a certain amount of silence (default is 1.0 seconds).
```python
# Start listening until 1.0s of silence
speech = aurora.Speech.listen()
# Or specify your own silence timeout (0.5 seconds shown here)
# speech = aurora.Speech.listen(silence_len=0.5)

# Convert to text
p = speech.text()
print(p.text) # prints the prediction
```

#### Continuously listen

Continuously listen and retrieve speech segments. Note: you can do anything with these speech segments, but here we'll convert them to text. Just like the previous example, these segments are demarcated by silence (1.0 second by default) and can be changed by passing the `silence_len` parameter. Additionally, you can make these segments fixed length (as in the example before the previous) by setting the `length` parameter.

```python
# Continuously listen and convert to speech (blocking example)
for speech in aurora.Speech.continuously_listen():
	p = speech.text()
	print(p.text)

# Reduce the amount of silence in between speech segments
for speech in aurora.Speech.continuously_listen(silence_len=0.5):
	p = speech.text()
	print(p.text)

# Fixed-length speech segments of 3 seconds
for speech in aurora.Speech.continuously_listen(length=3.0):
	p = speech.text()
	print(p.text)
```

### Interpret (Language Understanding)

The interpret service allows you to take any Aurora `Text` object and understand the user's intent and extract additional query information. Interpret can only be called on `Text` objects and return `Interpret` objects after completion. To convert a user's speech into and `Interpret` object, it must be converted to text first.

#### Basic example

```python
# create a Text object
text = aurora.Text("what is the time in los angeles")

# call the interpret service. This returns an `Interpret` object.
i = text.interpret()

# get the user's intent
print(i.intent)   # time

# get any additional information
print(i.entities) # { "location": "los angeles" }
```

#### User query example

```python
while True:
	# Repeatedly ask the user to enter a command
	user_text = raw_input("Enter a command:")
	if user_text == "quit":
		break
	
	# Interpret and print the results
	i = aurora.Text(user_text).interpret()
	print(i.intent, i.entities)
```

#### Smart Lamp

This example shows how easy it is to voice-enable a smart lamp. It responds to queries in the form of "turn on the lights" or "turn off the lamp". You define what `object` you're listening for (so that you can ignore queries like "turn on the music").

```python
valid_words = ["light", "lights", "lamp"]
valid_entities = lambda d: "object" in d and d["object"] in valid_words

for speech in aurora.Speech.continuously_listen(silence_len=0.5):
	i = speech.text().interpret()
	if i.intent == "turn_on" and valid_entities(i.entities):
		# do something to actually turn on the lamp
		print("Turning on the lamp")
	elif i.intent == "turn_off" and valid_entities(i.entities):
		# do something to actually turn off the lamp
		print("Turning off the lamp")
```


