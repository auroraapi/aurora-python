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
aurora.APP_ID    = "YOUR_APP_ID"    # put your app ID here
aurora.APP_TOKEN = "YOUR_APP_TOKEN" # put your app token here

# query the TTS service
speech = aurora.Text("Hello world").to_speech()

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
aurora.APP_ID    = "YOUR_APP_ID"    # put your app ID here
aurora.APP_TOKEN = "YOUR_APP_TOKEN" # put your app token here

# load a WAV file
a = aurora.audio.AudioFile.create_from_filename("test.wav")

# or open an already-open file
# with open("test.wav", "rb") as f:
#   a = aurora.audio.AudioFile.create_from_file(f)

p = aurora.Speech(a).to_text()
print(p.text) # 'hello world'
```

#### Convert a previous Text API call to Speech
```python
# Call the TTS API to convert "Hello world" to speech
speech = aurora.Text("Hello world").to_speech()

# Previous API returned a Speech object, so we can just call
# the to_text() method to get a prediction
p = speech.to_text()
print(p.text) # 'hello world'
```

#### Listen for a specified amount of time
```python
# Listen for 3 seconds (silence is automatically trimmed)
speech = aurora.Speech.listen(length=3)

# Convert to text
p = speech.to_text()
print(p.text) # prints the prediction
```

#### Listen for an unspecified amount of time

Calling this API will start listening and will automatically stop listening after a certain amount of silence (default is 2.5 seconds).
```python
# Start listening until 2.5s of silence
speech = aurora.Speech.listen()
# Or specify your own silence timeout (1 second shown here)
# speech = aurora.Speech.listen(silence_len=1.0)

# Convert to text
p = speech.to_text()
print(p.text) # prints the prediction
```

#### Continuously listen

Continuously listen and retrieve speech segments. Note: you can do anything with these speech segments, but here we'll convert them to text. Just like the previous example, these segments are demarcated by silence (2.5 seconds by default) and can be changed by passing the `silence_len` parameter. Additionally, you can make these segments fixed length (as in the example before the previous) by setting the `length` parameter.

```python
# Continuously listen and convert to speech (blocking example)
for speech in aurora.Speech.continuously_listen():
	p = speech.to_text()
	print(p.text)

# Reduce the amount of silence in between speech segments
for speech in aurora.Speech.continuously_listen(silence_len=1.0):
	p = speech.to_text()
	print(p.text)

# Fixed-length speech segments of 3 seconds
for speech in aurora.Speech.continuously_listen(length=3.0):
	p = speech.to_text()
	print(p.text)
```







