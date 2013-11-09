from cam import NetworkCamera
from cam import LocalCamera
from emailer import Mailer
from StringIO import StringIO
from config import Config
import base64

class GUI(object):
    NETWORK = 0
    LOCAL = 1
    def __init__(self):
        self.bufferedPic = None
        self.emailer = None
        self.camera = None
        self.Gtk = None
        self.GObject = None
        self.config = Config(filename="userSettings.json", autosave=True)
        try:
            self.config.load()
        except:
            print "Could not find user settings file: Making new one"
            self.config["cameraServerHistory"] = []
            self.config["gui"] = {}
        self.cameras = []

    def on_timeout(self, user_data):
        """
        Update value on the progress bar
        """
        if self.prbPreviewPulsing:
            self.prbPreview.pulse()
        else:
            self.prbPreview.set_fraction(0)
        if self.prbCameraPulsing:
            self.prbCamera.pulse()
        else:
            self.prbCamera.set_fraction(0)

        return True

    def setDefaults(self):
        self.prbPreview.set_text(" ")
        self.prbPreviewPulsing = False
        self.prbCamera.set_text(" ")
        self.prbCameraPulsing = False
        self.timeout_id = self.GObject.timeout_add(50, self.on_timeout, None)
        self.resetCameraNetworkStatus()
        self.reloadCamaraServerHistory()
        for guiSetting in self.config["gui"]:
            widget = self.__getattribute__(guiSetting)
            value = self.config["gui"][guiSetting]

            get_active = getattr(widget, "get_active", None)
            get_text = getattr(widget, "get_text", None)

            if callable(get_active):
                widget.set_active(value)
            elif callable(get_text): # is textbox
                if widget.get_visibility():
                    widget.set_text(value)
                else:
                    widget.set_text(base64.b64decode(value))

        # self.cameras = LocalCamera.getAvailableCameras()
        # localNumberModel = self.Gtk.ListStore(str, int)
        # for cameraNumber in cameras:
        #   localNumberModel.append([cameras[cameraNumber], cameraNumber])
        # self.cmbCameraLocalNumber.set_model(localNumberModel)
        # self.cmbCameraType.set_active(1)
        # self.cmbCameraLocalNumber.set_active(0)

    #Should add function for checkbox changed
    def settingChanged(self, widget, data=None):
        print "Changing ", widget.get_name()
        get_active = getattr(widget, "get_active", None)
        get_text = getattr(widget, "get_text", None)
        if callable(get_active):
            self.config["gui"][widget.get_name()] = widget.get_active()
        elif callable(get_text): # is textbox
            if widget.get_visibility():
                self.config["gui"][widget.get_name()] = widget.get_text()
            else:
                self.config["gui"][widget.get_name()] = base64.b64encode(widget.get_text())
        self.config.save()

    def resetCameraNetworkStatus(self):
        self.imgCameraReachedServer.set_from_icon_name("gtk-remove", self.Gtk.ICON_SIZE_BUTTON)
        self.imgCameraLoggedIn.set_from_icon_name("gtk-remove", self.Gtk.ICON_SIZE_BUTTON)
        self.imgCameraServerHasImage.set_from_icon_name("gtk-remove", self.Gtk.ICON_SIZE_BUTTON)
        self.imgCameraImageIsValid.set_from_icon_name("gtk-remove", self.Gtk.ICON_SIZE_BUTTON)
        self.tblCameraNetworkStatus.set_visible(False)

    def reloadLocalCameraCmb(self):
        CameraNumberModel = self.Gtk.ListStore(str, int)
        for cameraNumber in self.cameras:
            CameraNumberModel.append([self.cameras[cameraNumber], cameraNumber])
        self.cmbCameraLocalNumber.set_model(CameraNumberModel)
        self.cmbCameraLocalNumber.set_active(0)

    def reloadCamaraServerHistory(self):
        completion = self.Gtk.EntryCompletion()
        liststore = self.Gtk.ListStore(str)
        for s in self.config["cameraServerHistory"]:
            liststore.append([s])
        completion.set_model(liststore)
        self.txtCameraServerURL.set_completion(completion)
        completion.set_text_column(0)

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
            print "Sending image."
            buff = StringIO()
            emailFrom = self.txtEmailFrom.get_text()
            emailTo = self.txtEmailTo.get_text()
            emailSubject = self.txtEmailSubject.get_text()
            emailBody = self.txtEmailBody.get_text()
            emailImageName = self.txtEmailImageName.get_text()
            self.bufferedPic.save(buff, format="jpeg")
            buffStr = buff.getvalue()
            buff.close()
            self.emailer.sendMail(emailFrom, [emailTo], emailSubject, emailBody, [(emailImageName+".jpg", buffStr)])
            self.prbPreview.set_text("Email Sent.")
            print "Image sent."
        else:
            self.prbPreview.set_text("No Image: Take an Image.")
            print "No Image: Take an Image"
        self.prbPreviewPulsing = False

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
        self.tblCameraNetworkStatus.set_visible(True)
        url = self.txtCameraServerURL.get_text()
        username = self.txtCameraUsername.get_text()
        password = self.txtCameraPassword.get_text()
        try:
            if username:
                self.camera = NetworkCamera(url, username, password)
            else:
                self.camera = NetworkCamera(url)
        except:
            self.imgCameraReachedServer.set_from_icon_name("error", self.Gtk.ICON_SIZE_BUTTON)
            self.prbCameraPulsing = False
            return
        print "Network Connection: ", self.camera.canReachServer()
        if self.camera.canReachServer():
            self.imgCameraReachedServer.set_from_icon_name("gtk-apply", self.Gtk.ICON_SIZE_BUTTON)
        else:
            self.imgCameraReachedServer.set_from_icon_name("error", self.Gtk.ICON_SIZE_BUTTON)
            self.prbCameraPulsing = False
            return
        if self.camera.isGoodLogin():
            self.imgCameraLoggedIn.set_from_icon_name("gtk-apply", self.Gtk.ICON_SIZE_BUTTON)
        else:
            self.imgCameraLoggedIn.set_from_icon_name("error", self.Gtk.ICON_SIZE_BUTTON)
            self.prbCameraPulsing = False
            return
        if self.camera.serverHasFile():
            self.imgCameraServerHasImage.set_from_icon_name("gtk-apply", self.Gtk.ICON_SIZE_BUTTON)
        else:
            self.imgCameraServerHasImage.set_from_icon_name("error", self.Gtk.ICON_SIZE_BUTTON)
            self.prbCameraPulsing = False
            return
        if self.camera.imageIsGood():
            self.imgCameraImageIsValid.set_from_icon_name("gtk-apply", self.Gtk.ICON_SIZE_BUTTON)
        else:
            self.imgCameraImageIsValid.set_from_icon_name("error", self.Gtk.ICON_SIZE_BUTTON)
            self.prbCameraPulsing = False
            return

        history = self.config["cameraServerHistory"]
        history.append(url)
        self.reloadCamaraServerHistory()

        self.prbCameraPulsing = False

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

    def txtCameraNetworkChanged(self, textbox, data=None):
        self.resetCameraNetworkStatus()
