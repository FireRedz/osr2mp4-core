import io
from PIL import Image

from matplotlib import pyplot as plt
from osr2mp4.ImageProcess import imageproc
from osr2mp4.ImageProcess.Objects.RankingScreens.ARankingScreen import ARankingScreen


class RankingGraph(ARankingScreen):
	def __init__(self, frames, replay_info, settings):
		dummy = [Image.new("RGBA", (1, 1))]
		super().__init__(dummy, settings=settings)

		self.rankinggraph = frames[0]
		self.replay_info = replay_info

		if replay_info.is_perfect_combo:
			self.rankingperfect = frames[1]
		else:
			self.rankingperfect = Image.new("RGBA", (1, 1))

		self.rankingur = frames[2]

		# source: https://osu.ppy.sh/help/wiki/Skinning/Interface#ranking-screen
		if self.settings.skin_ini.general["Version"] == 1:
			self.y = 576
			self.perfectx = 320
		else:
			self.y = 608
			self.perfectx = 416

		self.generate_hp_graph()

	def generate_hp_graph(self):
		# professional code
		# how the fuck do i change the matplotlib resolution
		# the way i did it is just force resize it to the graph box size
		# which make the image quality terrible
		# TODO: make the thing not look terrible
		life = self.replay_info.life_bar_graph.split('|')
		life = [[float(_) for _ in e.split(',')] for e in life if len(e.split(',')) > 1 and e.split(',')[1]] # remove null shit
		life.sort(key=lambda x: x[1])

		x = [e[1] for e in life]
		y = [e[0] for e in life]


		fig = plt.figure(figsize=[9, 5], dpi=300)
		plt.axis('off')
		plt.margins(0, 0)
		plt.plot(x, y, color=(0, 1.0, 0), linewidth=4.0)
		plt.ylim(top=1)
		plt.ylim(bottom=0)

		plt.grid()

		buf = io.BytesIO()
		fig.savefig(buf, bbox_inches='tight', transparent="True", pad_inches=0)
		buf.seek(0)

		self.hp_graph = Image.open(buf).convert('RGBA')

		self.hp_graph = self.hp_graph.resize(
			(
				int(317*self.settings.scale),
				int(152*self.settings.scale),
				)
			)





	def add_to_frame(self, background):
		super().add_to_frame(background)
		if self.fade == self.FADEIN:
			imageproc.add(self.rankinggraph, background, 256 * self.settings.scale, self.y * self.settings.scale, self.alpha, topleft=True)
			imageproc.add(self.hp_graph, background, (256+1)*self.settings.scale, (self.y+10)*self.settings.scale, self.alpha, topleft=True)
			imageproc.add(self.rankingperfect, background, self.perfectx * self.settings.scale, 688 * self.settings.scale, self.alpha)
			imageproc.add(self.rankingur, background, (self.perfectx+225) * self.settings.scale, 688 * self.settings.scale, self.alpha ** 5)
			
