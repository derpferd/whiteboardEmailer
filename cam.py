from PIL import Image


cameras = {}
class LocalCamera(object):
    VIDEOCAPTUREDEVICECAMERA = 1
    OPENCVCAMERA = 2
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

    def __del__(self):
        for camera in cameras:
            try:
                camera.release()
            except:
                pass

    def getImage(self):
        if not cameras:
            self.getAvailableCameras()
        if self.cameraType == self.VIDEOCAPTUREDEVICECAMERA:
            from VideoCapture import Device
            if not self.__camera:
                self.__camera = cameras[self.number]
            return self.__camera.getImage()
        elif self.cameraType == self.OPENCVCAMERA:
            import cv2
            if not self.__camera:
                self.__camera = cameras[self.number]
                print "__camera", self.__camera
            (success, rawFrame) = self.__camera.read()
            if success:
                pilImage = Image.fromarray(rawFrame)
                return pilImage
            else:
                raise Exception("Camera Read did not work because")

    @staticmethod
    def getAvailableCameras():
        cams = {}
        try:
            from VideoCapture import Device
            device = True
            i = 0
            while device:

                if i in cameras:
                    cams.update({i: cameras[i].dev.getdisplayname()})
                else:
                    print "trying ", i
                    try:
                        device = Device(i)
                        cams.update({i: device.dev.getdisplayname()})
                        cameras.update({i: device})
                    except:
                        device = None
                i+=1
        except:
            try:
                import cv2.cv
                device = True
                i = 0
                while device:
                    if i in cameras:
                        cams.update({i: "/dev/video" + str(i)})
                    else:
                        print "trying ", i
                        device = cv2.VideoCapture(i)
                        if device.isOpened():
                            (s, f) = device.read()
                            print "read: ", s
                            cams.update({i: "/dev/video" + str(i)})
                            cameras.update({i: device})
                        else:
                            device = None
                    i+=1
            except:
                pass
        
        return cams


class NetworkCamera(object):
    """docstring for NetworkCamera"""
    def __init__(self, url, username=None, password=None):
        import re
        p = '(?P<pro>.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*)(?P<path>.*.)?'
        m = re.search(p, url)
        self.host = m.group("host")
        self.path = m.group("path")
        self.pro = m.group("pro")
        if self.pro == '':
            self.pro = "://"
        self.port = m.group("port")
        if self.port == '':
            self.port = 80
        else:
            self.port = int(self.port)
        self.url = self.pro + self.host + ":" + str(self.port) + self.path
        self.username = username
        self.password = password

    def canReachServer(self):
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((self.host, self.port))
        except socket.error:
            return False
        sock.close()
        return True

    def isGoodLogin(self):
        import urllib2
        try:
            mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
            mgr.add_password(None, self.url, self.username, self.password)
            opener = urllib2.build_opener(urllib2.HTTPBasicAuthHandler(mgr),
                                urllib2.HTTPDigestAuthHandler(mgr))
            print "Installing Opener..."
            urllib2.install_opener(opener)
            print "Connenting...",self.url
            fp = urllib2.urlopen(self.url)
        except urllib2.HTTPError as e:
            if e.msg == "basic auth failed" or e.msg == "Authorization Required":
                return False
        return True

    def serverHasFile(self):
        import urllib2
        try:
            mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
            mgr.add_password(None, self.url, self.username, self.password)
            opener = urllib2.build_opener(urllib2.HTTPBasicAuthHandler(mgr),
                                urllib2.HTTPDigestAuthHandler(mgr))
            print "Installing Opener..."
            urllib2.install_opener(opener)
            print "Connenting..."
            fp = urllib2.urlopen(self.url)
        except urllib2.HTTPError as e:
            if e.msg == "Not Found":
                return False
        return True

    def imageIsGood(self):
        try:
            self.getImage()
        except:
            return False
        return True

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
