from PIL import Image

from osr2mp4.ImageProcess.PrepareFrames.YImage import YImage
from osr2mp4.ImageProcess.Animation.alpha import fade

class Smoke:
	def __init__(self, settings: object):
		self.settings = settings
		self.frames = [YImage('cursor-smoke', settings).img]
		self.frames = [self.frames[0], *fade(self.frames[0], 1, 0, 1000, settings)]
		self.states = {}

	def add_to_frame(self, background: Image.Image, replay_info: object):
		cx, cy = replay_info[0], replay_info[1]
		key = replay_info[2]

		cx = int(cx * self.settings.playfieldscale) + self.settings.moveright
		cy = int(cy * self.settings.playfieldscale) + self.settings.movedown

		##  if key is touching the meme smoke button
		if key & 16:
			self.states[replay_info[3]] = (cx, cy)


		for time, pos in self.states.items():
			if time > replay_info[3]-9000: # not sure what the actual duration is, should be around ~8-10s
				
				""" ignore this, its for the smoke fadeout but currently its fucked so...
				if (time-(replay_info[3]-9500)) >= 8000:
					far_into = int(((9500-(time-(replay_info[3]-9500)))/1000)*40) # holy fuck
					frame = self.frames[far_into-1 if far_into < len(self.frames)-1 else len(self.frames)-1]
					
				else:
					frame = self.frames[0]
				"""

				smoke_size = frame.size

				x = int((pos[0] - smoke_size[0]/2))
				y = int((pos[1] - smoke_size[1]/2))


				background.paste(frame, (x, y), mask=frame)
		