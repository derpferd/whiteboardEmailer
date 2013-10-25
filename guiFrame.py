from cam import NetworkCamera
from cam import LocalCamera
from emailer import Mailer
from PIL import Image
from StringIO import StringIO

class GUI(object):
    NETWORK = 0
    LOCAL = 1
    def __init__(self):
        self.bufferedPic = None
        self.emailer = None
        self.camera = None
        self.Gtk = None
        self.Gdk = None
        self.prbPreviewPulsing = False
        self.cameras = []

    def setDefaults(self):
        self.prbPreview.set_text(" ")
        # self.cameras = LocalCamera.getAvailableCameras()
        # localNumberModel = self.Gtk.ListStore(str, int)
        # for cameraNumber in cameras:
        #   localNumberModel.append([cameras[cameraNumber], cameraNumber])
        # self.cmbCameraLocalNumber.set_model(localNumberModel)
        # self.cmbCameraType.set_active(1)
        # self.cmbCameraLocalNumber.set_active(0)

    def reloadLocalCameraCmb(self):
        CameraNumberModel = self.Gtk.ListStore(str, int)
        for cameraNumber in self.cameras:
            CameraNumberModel.append([self.cameras[cameraNumber], cameraNumber])
        self.cmbCameraLocalNumber.set_model(CameraNumberModel)
        self.cmbCameraLocalNumber.set_active(0)

    def run(self):
        self.Gtk.main()

    def onDeleteWindow(self, *args):
        self.Gtk.main_quit(*args)

    def btnUpdateClicked(self, button, data=None):
        print "updating.."
        self.prbPreviewPulsing = True
        self.prbPreview.set_text("Retrieving Image...")
        if self.camera == None:
            self.prbPreview.set_text("No camera connected. Please Goto Camera tab.")
            self.prbPreviewPulsing = False
            return
        img = self.camera.getImage()
        self.bufferedPic = img
        pixbuf = self.pilImageToPixbuf(img)

        self.imgPreview.set_from_pixbuf(pixbuf)
        self.prbPreview.set_text(" ")
        self.prbPreviewPulsing = False

    def btnSendEmailClicked(self, button, data=None):
        if self.bufferedPic:
            buff = StringIO()
            self.bufferedPic.save(buff, format="jpeg")
            buffStr = buff.getvalue()
            buff.close()
            email.sendMail("beau0307@d.umn.edu", ["123.jonathan@gmail.com"], "test attachment", "test", [("test.jpg", buffStr)])
        else:
            print "No Image: Take an Image"

    def btnEmailConnectClicked(self, button, data=None):
        print "Trying to connect to email server."
        self.lblEmailStatus.set_text("Connecting...")

        server = self.txtEmailServer.get_text()
        port = self.txtEmailPort.get_text()
        username = self.txtEmailUsername.get_text()
        password = self.txtEmailPassword.get_text()
        useTLS = self.swtEmailUseTLS.get_active()

        try:
            self.emailer = Mailer(server, port, username=username, password=password, useTLS=useTLS)
            self.emailer.tryConnection()
        except:
            print "Connection with server failed."
            self.lblEmailStatus.set_text("Connection with server failed.")
            self.emailer = None
            return

        try:
            self.emailer.tryLogin()
        except:
            print "Login Failed."
            self.lblEmailStatus.set_text("Login Failed.")
            self.emailer = None
            return

        print "Connection Working"
        self.lblEmailStatus.set_text("Connection Working.")

    def btnCameraNetworkConnectClicked(self, button, data=None):
        url = self.txtCameraServerURL.get_text()
        username = self.txtCameraUsername.get_text()
        password = self.txtCameraPassword.get_text()
        if username:
            self.camera = NetworkCamera(url, username, password)
        else:
            self.camera = NetworkCamera(url)

    def cmbCameraTypeChanged(self, combobox, data=None):
        print "Camera Type Changed"
        if self.cmbCameraType.get_active() == GUI.NETWORK:
            self.tblCameraNetwork.show()
            self.tblCameraLocal.hide()
        if self.cmbCameraType.get_active() == GUI.LOCAL:
            self.tblCameraNetwork.hide()
            self.tblCameraLocal.show()

    def cmbCameraLocalNumberChanged(self, combobox, data=None):
        print "Local Camera Changed"
        model = self.cmbCameraLocalNumber.get_model()
        row = model[self.cmbCameraLocalNumber.get_active_iter()]
        name, number = row[0], row[1]
        self.camera = LocalCamera(number)

    def btnCameraLocalReloadClicked(self, button, data=None):
        print "Reloading local Cameras"
        self.cameras = LocalCamera.getAvailableCameras()
        self.reloadLocalCameraCmb()


# def run():
#   builder = Gtk.Builder()
#   builder.add_from_file("main.glade")
#   builder.connect_signals(Handler())

#   window = builder.get_object("windowMain")
#   window.show_all()
#   Gtk.main()
#   print "Done."
