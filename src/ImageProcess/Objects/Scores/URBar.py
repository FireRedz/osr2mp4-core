from PIL import Image

from ImageProcess import imageproc
from ImageProcess.Objects.FrameObject import FrameObject


class URBar(FrameObject):
	def __init__(self, frames, settings):
		self.scale = settings.scale
		self.w, self.h = int(200 * settings.scale), int(25 * settings.scale)
		self.y = settings.height - self.h//2
		self.x = settings.width//2
		self.x_offset = self.x - self.w // 2

		self.bars = []
		self.resultdict = {50: 0, 100: 1, 300: 2}

		self.bar_container = Image.new("RGBA", (self.w, self.h))
		self.urbar, self.bar_images, self.maxtime = frames

	def add_bar(self, delta_t, hitresult):
		pos = int(self.w/2 + delta_t/self.maxtime * self.w/2)
		# self.bars.append([pos, 1, self.resultdict[hitresult]])
		img = self.bar_images[self.resultdict[hitresult]]
		imageproc.add(img, self.bar_container, pos, self.bar_container.size[1]//2)
		s = self.bar_container.size
		self.bar_container.paste((255, 255, 255, 255), (s[0]//2 - 1, 0, s[0]//2 + 1, s[1]))

	def add_to_frame_bar(self, background):
		img = self.urbar
		imageproc.add(img, background, self.x, self.y)
		img = Image.new("RGBA", (4, self.h), (255, 255, 255, 255))
		imageproc.add(img, background, self.x, self.y)

	def add_to_frame(self, background):
		img = self.bar_container
		imageproc.add(img, background, self.x_offset + self.w//2, self.y)
		imageproc.changealpha(self.bar_container, 0.999)
