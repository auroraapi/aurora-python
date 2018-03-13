import array, io, pyaudio, sys, time, wave
from pydub import AudioSegment, silence
from pydub.utils import make_chunks
from pyaudio import PyAudio

try:
	from StringIO import StringIO as BytesIO
except:
	from io import BytesIO

BUF_SIZE      = (2 ** 10)
SILENT_THRESH = (2 ** 11)
NUM_CHANNELS  = 1
FORMAT        = pyaudio.paInt16
RATE          = 16000

class AudioFile(object):
	"""
	AudioFile lets you play, manipulate, and create representations of WAV data.
	"""
	def __init__(self, audio):
		"""
		Creates an AudioFile.

		:param audio the raw WAV data (including header)
		:type string or byte array (anything that pydub.AudioSegment can accept)
		"""
		self.audio = AudioSegment(data=audio)
		self.should_stop = False
		self.playing = False

	def write_to_file(self, fname):
		"""
		Writes the WAV data to the specified location

		:param fname the file path to write to
		:type  fname string
		"""
		self.audio.export(fname, format="wav")

	def get_wav(self):
		"""
		Returns a byte string containing the WAV data encapsulated in this object.
		It includes the WAV header, followed by the WAV data.
		"""
		wav_data = BytesIO()
		wav = wave.open(wav_data, "wb")
		wav.setparams((self.audio.channels, self.audio.sample_width, self.audio.frame_rate, 0, 'NONE', 'not compressed'))
		wav.writeframes(self.audio.raw_data)
		wav.close()
		return wav_data.getvalue()

	def pad(self, seconds):
		"""
		Pads both sides of the audio with the specified amount of silence (in seconds)

		:param seconds the amount of silence to add (in seconds)
		:type  seconds float
		"""
		self.audio = AudioSegment.silent(duration=seconds*1000, frame_rate=16000) + self.audio + AudioSegment.silent(duration=seconds*1000, frame_rate=16000)
		return self

	def pad_left(self, seconds):
		"""
		Pads the left side of the audio with the specified amount of silence (in seconds)

		:param seconds the amount of silence to add (in seconds)
		:type  seconds float
		"""
		self.audio = AudioSegment.silent(duration=seconds*1000, frame_rate=16000) + self.audio
		return self

	def pad_right(self, seconds):
		"""
		Pads the right side of the audio with the specified amount of silence (in seconds)

		:param seconds the amount of silence to add (in seconds)
		:type  seconds float
		"""
		self.audio = self.audio + AudioSegment.silent(duration=seconds*1000, frame_rate=16000)
		return self

	def trim_silent(self):
		""" Trims extraneous silence at the ends of the audio """
		a = AudioSegment.empty()
		for seg in silence.detect_nonsilent(self.audio):
			a = a.append(self.audio[seg[0]:seg[1]], crossfade=0)

		self.audio = a
		return self

	def play(self):
		"""
		Plays the underlying audio on the default output device. Although this call
		blocks, you can stop playback by calling the stop() method
		"""
		p = pyaudio.PyAudio()
		stream = p.open(
			rate=self.audio.frame_rate,
			format=p.get_format_from_width(self.audio.sample_width),
			channels=self.audio.channels,
			output=True
		)

		self.playing = True
		for chunk in make_chunks(self.audio, 64):
			if self.should_stop:
				self.should_stop = False
				break
			stream.write(chunk.raw_data)

		self.playing = False
		stream.stop_stream()
		stream.close()
		p.terminate()

	def stop(self):
		""" Stop playback of the audio """
		if self.playing:
			self.should_stop = True

def record(length=0, silence_len=1.0):
	"""
	Records audio according to the given parameters and returns an instance of
	an AudioFile with the recorded audio
	"""
	data = array.array('h')
	for chunk in _pyaudio_record(length, silence_len):
		data.extend(chunk)

	p = pyaudio.PyAudio()
	wav_data = BytesIO()
	wav = wave.open(wav_data, "wb")
	wav.setparams((NUM_CHANNELS, p.get_sample_size(FORMAT), RATE, 0, 'NONE', 'not compressed'))
	wav.writeframes(data.tostring())
	wav.close()
	return AudioFile(wav_data.getvalue())
	
def stream(length=0, silence_len=1.0):
	"""
	Records audio, just like `record` does, except it doesn't return an AudioFile
	upon completion. Instead, it yields the WAV file (header + data) as it becomes
	available. Once caveat is that this function does not correctly populate the
	data size in the WAV header. As such, a WAV file generated from this should
	either be amended or should be read until EOF.
	"""
	# create fake WAV and yield it to get a WAV header
	p = pyaudio.PyAudio()
	wav_data = BytesIO()
	wav = wave.open(wav_data, "wb")
	wav.setparams((NUM_CHANNELS, p.get_sample_size(FORMAT), RATE, 0, 'NONE', 'not compressed'))
	wav.close()
	yield wav_data.getvalue()

	# yield audio until done listening
	for chunk in _pyaudio_record(length, silence_len):
		yield chunk.tostring()

def _is_silent(data):
	if len(data) == 0:
		return True
	return max(data) < SILENT_THRESH

def _pyaudio_record(length, silence_len):
	p = pyaudio.PyAudio()
	stream = p.open(
		rate=RATE,
		format=FORMAT,
		channels=NUM_CHANNELS,
		frames_per_buffer=BUF_SIZE,
		input=True,
		output=True,
	)

	data = array.array('h')
	while True:
		d = array.array('h', stream.read(BUF_SIZE, exception_on_overflow=False))
		if not _is_silent(d):
			break
		data.extend(d)
		if len(data) > 32 * BUF_SIZE:
			data = data[BUF_SIZE:]

	yield data

	silent_for = 0
	bytes_read = 0
	while True:
		d = array.array('h', stream.read(BUF_SIZE, exception_on_overflow=False))
		silent_for = silent_for + (len(d)/float(RATE)) if _is_silent(d) else 0
		bytes_read += len(d)
		yield d

		if length == 0 and silent_for > silence_len:
			break
		if length > 0 and bytes_read >= length*RATE:
			break

	stream.stop_stream()
	stream.close()
