import requests
from PIL import Image
from io import BytesIO


class ProfilePicture:
	def __init__(self, uid: int, settings: object):
		self.settings = settings
		self.pfp = self.prepare_profile_pic(uid, settings)

	def add_to_frame(self, background: Image):
		if self.settings.settings['Cool mode']:
			background.paste(self.pfp, (
				int(self.settings.width-self.pfp.size[0])//2,
				int(12*self.settings.scale)
				))

	@staticmethod
	def prepare_profile_pic(uid: int, settings: object):
		pfp_req = requests.get(f'https://a.ppy.sh/{uid}')

		if pfp_req.status_code != 200:
			pfp_req = requests.get('https://a.ppy.sh/')


		pfp = Image.open(BytesIO(pfp_req.content))
		pfp = pfp.resize(
			(
				int((75) * settings.scale),
				int((75) * settings.scale)
			)
			)

		return pfp