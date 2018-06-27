import pytest, mock, os, time, random, threading, tempfile
from tests.mocks import *
from auroraapi.audio import *
from auroraapi.audio import _is_silent, _pyaudio_record

class TestAudioFile(object):
  def setup(self):
    with open("tests/assets/hw.wav", "rb") as f:
      self.wav_data = f.read()

  def test_create(self):
    a = AudioFile(self.wav_data)
    assert isinstance(a, AudioFile)
    assert len(a.audio.raw_data) + 44 == len(self.wav_data)
  
  def test_write_to_file(self):
    path = os.path.join(tempfile.gettempdir(), "out.wav")
    a1 = AudioFile(self.wav_data)
    a1.write_to_file(path)

    with open(path, "rb")	as f:
      d2 = f.read()
      a2 = AudioFile(d2)
      assert d2 == self.wav_data
      assert a1.audio == a2.audio

    os.remove(path)

  def test_get_wav(self):
    a = AudioFile(self.wav_data)
    wav = a.get_wav()
    assert self.wav_data == wav
  
  def test_pad(self):
    a = AudioFile(self.wav_data)
    # adds 1s of padding to each side (2 x (16000 Hz * 16 bits/sample * 1 byte/8bits))
    pa = a.pad(1)
    wav = pa.get_wav()
    assert len(wav) == len(self.wav_data) + 64000
    assert wav[-1] == 0
    assert wav[44] == 0
    assert wav[44 + 32000] == self.wav_data[44]

  def test_pad_left(self):
    a = AudioFile(self.wav_data)
    # adds 1s of padding to left side (1 x (16000 Hz * 16 bits/sample * 1 byte/8bits))
    pa = a.pad_left(1)
    wav = pa.get_wav()
    assert len(wav) == len(self.wav_data) + 32000
    assert wav[-1] == self.wav_data[-1]
    assert wav[44] == 0
    assert wav[44 + 32000] == self.wav_data[44]
  
  def test_pad_right(self):
    a = AudioFile(self.wav_data)
    # adds 1s of padding to right side (1 x (16000 Hz * 16 bits/sample * 1 byte/8bits))
    pa = a.pad_right(1)
    wav = pa.get_wav()
    assert len(wav) == len(self.wav_data) + 32000
    assert wav[-1] == 0
    assert wav[44] == self.wav_data[44]
    assert wav[-32000] == 0
  
  def test_trim_silent(self):
    # replace all data with zeros:
    # d = [x for x in self.wav_data[44:]]
    d = self.wav_data[0:44] + bytes(r'\0' * len(self.wav_data[44:]), 'utf8')
    a = AudioFile(d)
    t = a.trim_silent()
    # TODO: actually add a test here. for now, it just checks for compilation
    # also, for some reason, trim_silent doesn't work, so figure that out
  
  def test_play(self):
    with mock.patch('pyaudio.PyAudio', new=MockPyAudio):
      a = AudioFile(self.wav_data)
      a.play()

      # for some reason, a.play() plays a couple of extra bytes, so we can't do
      # an exact equality check here
      assert len(MockStream.data) >= len(self.wav_data[44:])
      assert (len(MockStream.data) - len(self.wav_data[44:]))/len(MockStream.data) < 0.001 
    MockStream.reset_data()

  def test_play_stop(self):
    def stop_audio(timeout, audio):
      time.sleep(timeout)
      audio.stop()
    
    def play_audio(audio):
      audio.play()

    with mock.patch('pyaudio.PyAudio', new=MockPyAudio):
      a = AudioFile(self.wav_data)
      
      t1 = threading.Thread(target=play_audio, args=(a,))
      t2 = threading.Thread(target=stop_audio, args=(0.1, a))

      t1.start()
      t2.start()
      t1.join()
      t2.join()

      # we stopped playback after 0.1 seconds, so expect the stream audio len
      # to be much less than the input audio len (TODO: make this more precise)
      assert len(MockStream.data) < len(self.wav_data[44:])
      assert (len(MockStream.data) - len(self.wav_data[44:]))/len(self.wav_data[44:]) < 0.5
    MockStream.reset_data()

class TestAudio(object):
  def setup(self):
    with open("tests/assets/hw.wav", "rb") as f:
      self.wav_data = f.read()
  
  def test_record(self):
    with mock.patch('auroraapi.audio._pyaudio_record', new=mock_pyaudio_record):
      a = record()
      assert a.get_wav() == self.wav_data

  def test_stream(self):
    with mock.patch('auroraapi.audio._pyaudio_record', new=mock_pyaudio_record):
      first = True
      header = []
      data = []
      count = 0
      for chunk in stream():
        if first:
          header = chunk
          first = False
        data.extend(chunk)
      
      assert len(header) == 44
      assert len(data) == len(self.wav_data)
  
  def test__is_silent_empty(self):
    assert _is_silent([])
  
  def test__is_silent_quiet(self):
    assert _is_silent([random.randint(0, SILENT_THRESH - 1) for i in range(1024)])
  
  def test__is_silent_mixed(self):
    assert not _is_silent([random.randint(0, 2*SILENT_THRESH) for i in range(1024)])
  
  def test__is_silent_loud(self):
    assert not _is_silent([random.randint(SILENT_THRESH//2, 3*SILENT_THRESH) for i in range(1024)])

  def test__pyaudio_record_silence(self):
    # set record mode to silent, and start loud, so that we don't infinitly
    # remove silent data
    MockStream.read_mode = "silent"
    MockStream.start_loud = True
    with mock.patch('pyaudio.PyAudio', new=MockPyAudio):
      # should record up to 1 second of silence
      data = []
      for chunk in _pyaudio_record(0, 1.0):
        data.extend(chunk)
      assert len(data) == 16384

  def test__pyaudio_record_mixed(self):
    # set record mode to random noise
    MockStream.read_mode = "random"
    with mock.patch('pyaudio.PyAudio', new=MockPyAudio):
      # should record up to 1 second of silence
      data = []
      for chunk in _pyaudio_record(1.0, 0):
        data.extend(chunk)
      assert len(data) >= 16384
  
  def test__pyaudio_record_loud(self):
    # set record mode to loud
    MockStream.read_mode = "loud"
    with mock.patch('pyaudio.PyAudio', new=MockPyAudio):
      # should record up to 1 second of silence
      data = []
      for chunk in _pyaudio_record(1.0, 0):
        data.extend(chunk)
      assert len(data) == 16384
  
  
