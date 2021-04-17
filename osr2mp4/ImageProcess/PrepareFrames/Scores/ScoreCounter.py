from osr2mp4.ImageProcess import imageproc


def prepare_scorecounter(scorenumber: list, settings: object):
	"""
	:param scorenumber: ScoreNumber
	:return: [PIL.Image]
	"""
	img = []
	resize_val = 0.87 if not settings.settings['Cool mode'] else 0.55
	for image in scorenumber.score_images:
		imgscore = imageproc.change_size(image.img, resize_val, resize_val)
		img.append(imgscore)
	return img
