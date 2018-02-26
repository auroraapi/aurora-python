import pytest, os, tempfile
from auroraapi.audio import *

class TestAudioFile(object):
	def test_create(self):
		with open("tests/assets/hw.wav", "rb") as f:
			d = f.read()
			a = AudioFile(d)
			assert isinstance(a, AudioFile)
			assert len(a.audio.raw_data) + 44 == len(d)
	
	def test_write_to_file(self):
		path = os.path.join(tempfile.gettempdir(), "out.wav")
		with open("tests/assets/hw.wav", "rb") as f:
			d1 = f.read()
			a1 = AudioFile(d1)
			a1.write_to_file(path)

			with open(path, "rb")	as f:
				d2 = f.read()
				a2 = AudioFile(d2)
				assert d2 == d1
				assert a1.audio == a2.audio

		os.remove(path)

	def test_get_wav(self):
		with open("tests/assets/hw.wav", "rb") as f:
			d = f.read()
			a = AudioFile(d)
			w = a.get_wav()
			assert d == w
	
	def test_pad(self):
		with open("tests/assets/hw.wav", "rb") as f:
			d = f.read()
			a = AudioFile(d)
			# adds 1s of padding to each side (2 x (16000 Hz * 16 bits/sample * 1 byte/8bits))
			pa = a.pad(1)
			w = pa.get_wav()
			assert len(w) == len(d) + 64000
			assert w[-1] == 0
			assert w[44] == 0
			assert w[44 + 32000] == d[44]

	def test_pad_left(self):
		with open("tests/assets/hw.wav", "rb") as f:
			d = f.read()
			a = AudioFile(d)
			# adds 1s of padding to left side (1 x (16000 Hz * 16 bits/sample * 1 byte/8bits))
			pa = a.pad_left(1)
			w = pa.get_wav()
			assert len(w) == len(d) + 32000
			assert w[-1] == d[-1]
			assert w[44] == 0
			assert w[44 + 32000] == d[44]
	
	def test_pad_right(self):
		with open("tests/assets/hw.wav", "rb") as f:
			d = f.read()
			a = AudioFile(d)
			# adds 1s of padding to right side (1 x (16000 Hz * 16 bits/sample * 1 byte/8bits))
			pa = a.pad_right(1)
			w = pa.get_wav()
			assert len(w) == len(d) + 32000
			assert w[-1] == 0
			assert w[44] == d[44]
			assert w[-32000] == 0
	
	def test_trim_silent(self):
		with open("tests/assets/hw.wav", "rb") as f:
			d = f.read()
			a = AudioFile(d)
			t = a.trim_silent()
			# TODO: actually add a test here. for now, it just checks for compilation
	
	# def test_play(self):


