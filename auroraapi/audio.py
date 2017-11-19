import io, wave, pyaudio

class AudioFile(object):
	def __init__(self, data):
		self.data = data

	def write_to_file(self, fname):
		with open(fname, 'wb') as f:
			f.write(self.data)

	def play(self):
		bfr = io.BytesIO(self.data)
		wf = wave.openfp(bfr, 'rb')

		p = pyaudio.PyAudio()
		stream = p.open(
			format=p.get_format_from_width(wf.getsampwidth()),
			channels=wf.getnchannels(),
			rate=wf.getframerate(),
			output=True
		)

		while True:
			data = wf.readframes(512)
			stream.write(data)
			if len(data) == 0:
				break

		stream.stop_stream()
		stream.close()
		p.terminate()

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
