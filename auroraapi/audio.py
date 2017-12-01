import array, io, pyaudio, sys, time, wave
import StringIO

BUF_SIZE      = (2 ** 10)
MAX_THRESH    = (2 ** 14)
SILENT_THRESH = (2 ** 10)
NUM_CHANNELS  = 1
FORMAT        = pyaudio.paInt16
RATE          = 16000

class AudioFile(object):
	def __init__(self, buff):
		self.data = buff

	def write_to_file(self, fname):
		with open(fname, 'wb') as f:
			f.write(self.data)

	def get_wav_frames(self):
		wav_data = io.BytesIO(self.data)
		wav_file = wave.open(wav_data, 'rb')
		return wav_file.readframes(wav_file.getnframes())

	def set_data(self, data):
		old_wav_data = io.BytesIO(self.data)
		old_wav_file = wave.open(old_wav_data, 'rb')

		new_wav_data = StringIO.StringIO()
		new_wav_file = wave.open(new_wav_data, 'wb')
		new_wav_file.setparams(old_wav_file.getparams())
		new_wav_file.writeframes(data)
		new_wav_file.close()

		self.data = new_wav_data.getvalue()
		return self

	def pad(self, seconds):
		return self.pad_left(seconds).pad_right(seconds)

	def pad_left(self, seconds):
		d = self.get_wav_frames()
		d = "".join([chr(0) for i in range(int(seconds*RATE))]) + d
		return self.set_data(d)

	def pad_right(self, seconds):
		d = self.get_wav_frames()
		d = d + "".join([chr(0) for i in range(int(seconds*RATE))])
		return self.set_data(d)

	def trim_silent(self):
		d = array.array('h', self.get_wav_frames())
		left, right = 0, len(d) - 1
		while left < right:
			if abs(d[left]) > SILENT_THRESH:
				break
			left += 1
		while right > left:
			if abs(d[right]) > SILENT_THRESH:
				break
			right -= 1

		return self.set_data((d[left:right]).tostring())

	def play(self):
		bfr = io.BytesIO(self.data)
		wf = wave.openfp(bfr, 'rb')

		p = pyaudio.PyAudio()
		stream = p.open(
			rate=wf.getframerate(),
			format=p.get_format_from_width(wf.getsampwidth()),
			channels=wf.getnchannels(),
			output=True
		)

		while True:
			data = wf.readframes(BUF_SIZE)
			stream.write(data)
			if len(data) == 0:
				break

		stream.stop_stream()
		stream.close()
		p.terminate()
		return self

	@staticmethod
	def from_recording(length=0, silence_len=2.5):
		p = pyaudio.PyAudio()
		stream = p.open(
			rate=RATE,
			format=FORMAT,
			channels=NUM_CHANNELS,
			input=True,
			output=True,
			frames_per_buffer=BUF_SIZE
		)

		data = array.array('h')
		if length == 0:
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
		return AudioFile(wav_data.getvalue())

	@staticmethod
	def create_from_wav_data(d):
		return AudioFile(d)

	@staticmethod
	def create_from_file(f):
		return AudioFile(f.read())

	@staticmethod
	def create_from_filename(f):
		with open(f, 'rb') as file:
			return AudioFile(file.read())

	@staticmethod
	def create_from_stream(s):
		return AudioFile(s.readall())

	@staticmethod
	def create_from_http_stream(s):
		return AudioFile(s.read())

def is_silent(data):
	return max(data) < SILENT_THRESH
