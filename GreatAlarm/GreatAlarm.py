from gtts import gTTS
from osax import *
import time
import datetime
import subprocess
import uuid
import thread


class GreatAlarm():
	def __init__(self, warninig_text, starting_time):
		self.starting_time = starting_time
		self.sound_path = self.create_sound(warninig_text)
		self.check()

	def hm_extractor(self):
		segs = self.starting_time.split(":")
		return [int(segs[0]), int(segs[1])]

	def check(self):
		now = datetime.datetime.now()
		time_target = self.hm_extractor()
		while(1):
			if now.hour >= time_target[0] and now.minute >= time_target[1]:
				self.boom()

	def boom(self):
		thread.start_new_thread(self.volume_watcher, ())
		while(1):
			subprocess.call(["afplay", self.sound_path])

	def create_sound(self, warning_text):
		mid_path = "./hello.mp3"
		tts = gTTS(text=warning_text, lang='en')
		tts.save(mid_path)

		filename = str(uuid.uuid4())+".wav"
		subprocess.call(['ffmpeg', '-i', mid_path, filename])
		return filename

	def volume_watcher(self):
		sa = OSAX()
		while(1):
			sa.set_volume(100)
			time.sleep(1)