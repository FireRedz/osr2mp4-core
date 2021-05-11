from PIL import Image

from osr2mp4.ImageProcess.Animation.alpha import fadein, fade
from osr2mp4.ImageProcess.Animation.size import grow, resize
from osr2mp4.ImageProcess.Animation import easings
from osr2mp4.ImageProcess import imageproc
from osr2mp4.ImageProcess.PrepareFrames.YImage import YImage, YImages

sliderb = "sliderb"
sliderfollowcircle = "sliderfollowcircle"
sliderscorepoint = "sliderscorepoint"
reversearrow = "reversearrow"
default_size = 128


def ballinhole(follow: Image, sliderball: Image):

	if follow.size[0] < sliderball.size[0] or follow.size[1] < sliderball.size[1]:
		width, height = max(follow.size[0], sliderball.size[0]), max(follow.size[1], sliderball.size[1])
		f = Image.new("RGBA", (width, height))
		imageproc.add(follow, f, width//2, height//2)
		follow = f

	y1 = (follow.size[1] - sliderball.size[1]) // 2
	x1 = (follow.size[0] - sliderball.size[0]) // 2

	follow.paste(sliderball, (x1, y1), sliderball)
	return follow


def load(scale: float, settings: 'Settings'):
	arrow_frames = []
	for x in range(120, 100, -4):
		img = YImage(reversearrow, settings, scale * x / 100, rotate=1)
		arrow_frames.append(img.img)

	sliderb_frames = YImages(sliderb, settings, scale).frames
	sliderfollow_frames = YImages(sliderfollowcircle, settings, scale).frames
	slider_tick = YImage(sliderscorepoint, settings, scale).img
	return arrow_frames, sliderb_frames, sliderfollow_frames, slider_tick


def prepare_slider(diff: dict, scale: float, settings: 'Settings'):

	cs = (54.4 - 4.48 * diff["CircleSize"]) * scale
	radius_scale = cs * 2 / default_size

	interval = settings.timeframe / settings.fps
	follow_fadein = 160  # need 160ms to fadein

	arrow_frames, sliderb_frames, sliderfollow_frames, slider_tick = load(radius_scale, settings)

	bframes = []

	for c in range(1, settings.skin_ini.colours["ComboNumber"] + 1):
		bframes += [[]]

		color = settings.skin_ini.colours["Combo" + str(c)]
		for x in range(len(sliderb_frames)):
			if settings.skin_ini.general["AllowSliderBallTint"]:
				color_sb = imageproc.add_color(sliderb_frames[x], color)
			else:
				color_sb = sliderb_frames[x].copy()
			bframes[-1].append(color_sb)

	sframes = resize(sliderfollow_frames[0], 0.5, 1, 180, settings, easings.easeOutQuad)
	sframes = fade(sframes, 0, 1, 60, settings)
	sframes = sframes[::-1]


	sliderfollow_fadeout = fade(sliderfollow_frames[0], 1, 0, 200, settings, easings.easeInQuad)
	sliderfollow_fadeout = resize(sliderfollow_fadeout, 1, 0.8, 200, settings, easings.easeOutQuad)


	return arrow_frames, sframes, sliderfollow_fadeout, slider_tick, bframes
