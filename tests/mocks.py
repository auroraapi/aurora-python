import array, time, random
from auroraapi.audio import AudioFile

def mock_pyaudio_record(a, b):
	with open("tests/assets/hw.wav", "rb") as f:
		yield array.array('h', AudioFile(f.read()).audio.raw_data)

class MockStream(object):
	data = []
	start_loud = True
	read_mode = "silent"

	def write(self, d):
		MockStream.data.extend(d)
		# simulate some delay in writing the stream 
		time.sleep(0.01)
		return len(d)
	
	def read(self, size, **kwargs):
		if MockStream.start_loud:
			MockStream.start_loud = False
			return [random.randint(2048, 8192) for i in range(size)]
		if MockStream.read_mode == "silent":
			return [random.randint(0, 1023) for i in range(size)]
		if MockStream.read_mode == "random":
			return [random.randint(0, 4096) for i in range(size)]
		if MockStream.read_mode == "loud":
			return [random.randint(2048, 8192) for i in range(size)]
		return []

	def stop_stream(self):
		return

	def close(self):
		return

	@staticmethod
	def reset_data():
		MockStream.data = []

class MockPyAudio(object):
	def open(self, **kwargs):
		return MockStream()
	def get_format_from_width(self, width):
		return width
	def terminate(self):
		return
