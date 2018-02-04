from pydub import AudioSegment, silence
from pydub.utils import make_chunks
from pyaudio import PyAudio
import array, io, pyaudio, sys, time, wave
import StringIO

BUF_SIZE      = (2 ** 10)
MAX_THRESH    = (2 ** 14)
SILENT_THRESH = (2 ** 10)
NUM_CHANNELS  = 1
FORMAT        = pyaudio.paInt16
RATE          = 16000

class AudioFile(object):
	def __init__(self, audio):
		self.audio = audio
		self.shouldStop = False

	def write_to_file(self, fname):
		self.audio.export(fname, format="wav")

	def get_wav(self):
		wav_data = StringIO.StringIO()
		wav = wave.open(wav_data, "wb")
		wav.setparams((self.audio.channels, self.audio.sample_width, self.audio.frame_rate, 0, 'NONE', 'not compressed'))
		wav.writeframes(self.audio.raw_data)
		wav.close()
		return wav_data.getvalue()

	def pad(self, seconds):
		self.audio = AudioSegment.silent(duration=seconds*1000, frame_rate=16000) + self.audio + AudioSegment.silent(duration=seconds*1000, frame_rate=16000)
		return self

	def pad_left(self, seconds):
		self.audio = AudioSegment.silent(duration=seconds*1000, frame_rate=16000) + self.audio
		return self

	def pad_right(self, seconds):
		self.audio = self.audio + AudioSegment.silent(duration=seconds*1000, frame_rate=16000)
		return self

	def trim_silent(self):
		a = AudioSegment.empty()
		for seg in silence.detect_nonsilent(self.audio):
			a = a.append(self.audio[seg[0]:seg[1]], crossfade=0)

		self.audio = a
		return self

	def play(self):
		p = pyaudio.PyAudio()
		stream = p.open(
			rate=self.audio.frame_rate,
			format=p.get_format_from_width(self.audio.sample_width),
			channels=self.audio.channels,
			output=True
		)

		for chunk in make_chunks(self.audio, 64):
			if self.shouldStop:
				self.shouldStop = False
				break
			stream.write(chunk.raw_data)

		stream.stop_stream()
		stream.close()
		p.terminate()
		return self

	def stop(self):
		self.shouldStop = True

	@staticmethod
	def from_recording(length=0, silence_len=1.0):
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
		while len(data) == 0 or is_silent(data):
			data = array.array('h', stream.read(BUF_SIZE, exception_on_overflow=False))

		silent_for = 0
		while True:
			d = array.array('h', stream.read(BUF_SIZE, exception_on_overflow=False))
			silent_for = silent_for + (len(d)/float(RATE)) if is_silent(d) else 0
			data.extend(d)

			if length == 0 and silent_for > silence_len:
				break
			if length > 0 and len(data) >= length*RATE:
				break

		wav_data = StringIO.StringIO()
		wav = wave.open(wav_data, "wb")
		wav.setparams((NUM_CHANNELS, p.get_sample_size(FORMAT), RATE, 0, 'NONE', 'not compressed'))
		wav.writeframes(data.tostring())
		wav.close()
		return AudioFile.create_from_wav_data(wav_data.getvalue())

	@staticmethod
	def create_from_wav_data(d):
		return AudioFile(AudioSegment(data=d))

	@staticmethod
	def create_from_file(f):
		return AudioFile(AudioSegment(data=f.read()))

	@staticmethod
	def create_from_filename(f):
		return AudioFile(AudioSegment.from_file(f, format="wav"))

	@staticmethod
	def create_from_stream(s):
		return AudioFile(AudioSegment(data=s.readall()))

	@staticmethod
	def create_from_http_stream(s):
		return AudioFile(AudioSegment(data=s.read()))

def is_silent(data):
	return max(data) < SILENT_THRESH
