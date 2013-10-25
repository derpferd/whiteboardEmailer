from gi.repository import Gtk
from gi.repository import GdkPixbuf
from gi.repository import Gdk
from gi.repository import GObject
# from cam import NetworkCamera
# from emailer import Mailer
# from PIL import Image
# from StringIO import StringIO
from guiFrame import GUI
import threading

class MainGUI(GUI):
    def __init__(self):
        Gdk.threads_init()
        super(MainGUI, self).__init__()
        builder = Gtk.Builder()
        builder.add_from_file("mainGtk3.glade")
        builder.connect_signals(self)

        window = builder.get_object("windowMain")
        window.show_all()

        self.Gtk = Gtk
        self.lblEmailStatus = builder.get_object("lblEmailStatus")
        self.txtEmailServer = builder.get_object("txtEmailServer")
        self.txtEmailPort = builder.get_object("txtEmailPort")
        self.txtEmailUsername = builder.get_object("txtEmailUsername")
        self.txtEmailPassword = builder.get_object("txtEmailPassword")
        self.swtEmailUseTLS = builder.get_object("swtEmailUseTLS")
        self.imgPreview = builder.get_object("imgPreview")
        self.lblCameraStatus = builder.get_object("lblCameraStatus")
        self.cmbCameraType = builder.get_object("cmbCameraType")
        self.cmbCameraLocalNumber = builder.get_object("cmbCameraLocalNumber")
        self.tblCameraNetwork = builder.get_object("tblCameraNetwork")
        self.tblCameraLocal = builder.get_object("tblCameraLocal")
        self.txtCameraServerURL = builder.get_object("txtCameraServerURL")
        self.txtCameraUsername = builder.get_object("txtCameraUsername")
        self.txtCameraPassword = builder.get_object("txtCameraPassword")
        self.prbPreview = builder.get_object("prbPreview")

        cameraTypesStore = Gtk.ListStore(str)
        cameraTypesStore.append(["Network"])
        cameraTypesStore.append(["Local"])

        self.cmbCameraType.set_model(cameraTypesStore)
        self.cmbCameraType.set_active(0)

        cell = Gtk.CellRendererText()
        self.cmbCameraType.pack_start(cell, True)
        self.cmbCameraType.add_attribute(cell, "text", 0)

        super(MainGUI, self).setDefaults()
        self.setDefaults()

        self.timeout_id = GObject.timeout_add(50, self.on_timeout, None)

    def setDefaults(self):
        CameraNumberModel = self.Gtk.ListStore(str, int)
        self.cmbCameraLocalNumber.set_model(CameraNumberModel)
        cell = Gtk.CellRendererText()
        self.cmbCameraLocalNumber.pack_start(cell, True)
        self.cmbCameraLocalNumber.add_attribute(cell, "text", 0)

    def pilImageToPixbuf(self, img):
        import StringIO
        if img.mode != 'RGB':
            img = img.convert('RGB')
        buff = StringIO.StringIO()
        img.save(buff, 'ppm')
        contents = buff.getvalue()
        buff.close()
        loader = GdkPixbuf.PixbufLoader.new_with_type('pnm')
        loader.write(contents)
        pixbuf = loader.get_pixbuf()
        loader.close()
        return pixbuf

    def on_timeout(self, user_data):
        """
        Update value on the progress bar
        """
        if self.prbPreviewPulsing:
            self.prbPreview.pulse()
        else:
            self.prbPreview.set_fraction(0)

        return True

    def btnUpdateClicked(self, widget, data=None):
        print "starting new thread"
        self.prbPreviewPulsing = True
        threading.Thread(target=super(MainGUI, self).btnUpdateClicked, args=(widget, data)).start()

def run():
    MainGUI()
    Gdk.threads_enter()
    Gtk.main()
    Gdk.threads_leave()
    print "Done."
