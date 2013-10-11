

class Camera(object):
	VIDEOCAPTUREDEVICECAMERA = 0
	OPENCVCAMERA = 1
	"""docstring for Camera"""
	def __init__(self, number=0):
		self.cameraType = -1
		try:
			from VideoCapture import Device
			self.cameraType = self.VIDEOCAPTUREDEVICECAMERA
		except Exception, e:
			try:
				import cv2.cv
				self.cameraType = self.OPENCVCAMERA
			except Exception, e:
				pass
			pass
		if self.cameraType == -1:
			raise ImportError("Can not load a library to access camera.")

		self.number = number
		self.__camera = False

	def getImage(self):
		if self.cameraType == self.VIDEOCAPTUREDEVICECAMERA:
			from VideoCapture import Device
			if not self.__camera:
				self.__camera = Device(self.number)
			return self.__camera.getImage()
		elif self.cameraType == self.OPENCVCAMERA:
			import cv2.cv
			self.__camera = cv.CaptureFromCAM(0)
			rawFrame = cv.QueryFrame(self.__camera)
			return rawFrame


class NetworkCamera(object):
	"""docstring for NetworkCamera"""
	def __init__(self, url, username=None, password=None):
		self.url = url
		self.username = username
		self.password = password


	def getImage(self):
		import urllib2
		from PIL import Image
		from cStringIO import StringIO
		mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
		mgr.add_password(None, self.url, self.username, self.password)
		opener = urllib2.build_opener(urllib2.HTTPBasicAuthHandler(mgr),
							urllib2.HTTPDigestAuthHandler(mgr))
		print "Installing Opener..."
		urllib2.install_opener(opener)
		print "Connenting..."
		fp = urllib2.urlopen(self.url)
		print "Downloading Image..."
		lines = fp.read()
		buff = StringIO(lines)
		fp.close()
		print "Creating Image..."
		return Image.open(buff)
