# Aurora Python SDK


## Overview

Aurora is the enterprise end-to-end speech solution. This Python SDK will allow you to quickly and easily use the Aurora service to integrate voice capabilities into your application.

The SDK is currently in a pre-alpha release phase. Bugs and limited functionality should be expected.

## Installation

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
audio = aurora.TTS.text_to_speech("Hello world")

# play the resulting audio
audio.play()

# or save it to a file
audio.write_to_file("test.wav")
```


