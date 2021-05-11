"""

	Certified bruh moment code, yuitora pls help, i cant math man.

"""
import numpy as np
from PIL import Image

from osr2mp4.ImageProcess import imageproc
from osr2mp4.ImageProcess.PrepareFrames.YImage import YImage
from osr2mp4.ImageProcess.Animation.alpha import fade
from osr2mp4.ImageProcess.Animation import easings

class Smoke:
	def __init__(self, settings: object):
		self.settings = settings
		self.frames = [YImage('cursor-smoke', settings, 0.5).img]
		self.frames = [self.frames[0], *fade(self.frames[0], 1, 0, 1000, settings, easings.easeInQuad)]
		self.states = {}


	def add_to_frame(self, background: Image.Image, replay_info: object):
		return # disable smokes for now

		cx, cy = replay_info.x, replay_info.y
		key = replay_info.keys_pressed

		cx = int(cx * self.settings.playfieldscale) + self.settings.moveright
		cy = int(cy * self.settings.playfieldscale) + self.settings.movedown

		## if key is touching the meme smoke button
		if key & 16:
			self.states[replay_info.time] = (cx, cy)


		before = [cx, cy, replay_info.time]

		# reduce
		self.states = {time: pos for time, pos in self.states.items() if time > replay_info.time - 9000}

		for time, pos in self.states.items():
			if time > replay_info.time - 9000: # not sure what the actual duration is, should be around ~8-10s
				
				if (replay_info.time - time) >= 8000:
					far_into = int((((replay_info.time - time) % 8000)/1000)*len(self.frames)-1) # peak programming
					frame = self.frames[far_into]
				else:
					frame = self.frames[0]

				smoke_size = frame.size
				duration = max(time - before[2], 1)
				for time in np.arange(0, duration, self.settings.timeframe/self.settings.fps): # make inbetween (?)
					x = easings.easeLinear(time, before[0], pos[0]-before[0], duration)
					y = easings.easeLinear(time, before[1], pos[1]-before[1], duration)

					x = int((x - smoke_size[0]/2))
					y = int((y - smoke_size[1]/2))
					imageproc.add(frame, background, x, y, topleft=True)

				before = [*pos, time]


			
		