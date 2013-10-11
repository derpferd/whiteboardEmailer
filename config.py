import json

class Config(object):
	"""Config is a class for holding all user configurations"""
	def __init__(self):
		self.emailServer = None
		self.emailPort = None
		self.emailUsername = None
		self.emailPassword = None
		self.emailUseTLS = None
		self.emailFrom = None
		self.emailTo = None
		self.emailSubject = None
		self.emailText = None
		self.networkCameraURL = None
		self.networkCameraUsername = None
		self.networkCameraPassword = None
		self.videoCaptureCameraNumber = None
		self.imageFormat = None
		self.imageName = None
