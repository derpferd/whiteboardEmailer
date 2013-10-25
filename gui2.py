import sys

try:
    import pygtk
    pygtk.require("2.0")
except:
    pass
try:
    import gtk
    import gtk.glade
    import gtk.gdk
except:
    raise ImportError("Could not find dependency: gtk")
    sys.exit(1)

from guiFrame import GUI
import threading


class MainGUI(GUI):
    wTree = None
    def __init__(self):
        gtk.gdk.threads_init()
        super(MainGUI, self).__init__()
        self.wTree = gtk.glade.XML( "mainGtk2L.glade" )
        self.Gtk = gtk
        
        dic = {
            "onDeleteWindow": self.onDeleteWindow,
            "btnEmailConnectClicked": self.btnEmailConnectClicked,
            "btnCameraNetworkConnectClicked": self.btnCameraNetworkConnectClicked,
            "btnUpdateClicked": self.btnUpdateClicked,
            "cmbCameraTypeChanged": self.cmbCameraTypeChanged,
            "cmbCameraLocalNumberChanged": self.cmbCameraLocalNumberChanged,
            "btnCameraLocalReloadClicked": self.btnCameraLocalReloadClicked
        }
        
        self.wTree.signal_autoconnect( dic )
        self.lblEmailStatus = self.wTree.get_widget("lblEmailStatus")
        self.txtEmailServer = self.wTree.get_widget("txtEmailServer")
        self.txtEmailPort = self.wTree.get_widget("txtEmailPort")
        self.txtEmailUsername = self.wTree.get_widget("txtEmailUsername")
        self.txtEmailPassword = self.wTree.get_widget("txtEmailPassword")
        self.swtEmailUseTLS = self.wTree.get_widget("swtEmailUseTLS")
        self.imgPreview = self.wTree.get_widget("imgPreview")
        self.tblCameraNetwork = self.wTree.get_widget("tblCameraNetwork")
        self.tblCameraLocal = self.wTree.get_widget("tblCameraLocal")
        self.cmbCameraLocalNumber = self.wTree.get_widget("cmbCameraLocalNumber")
        self.cmbCameraType = self.wTree.get_widget("cmbCameraType")
        self.lblCameraStatus = self.wTree.get_widget("lblCameraStatus")
        self.prbPreview = self.wTree.get_widget("prbPreview")

        super(MainGUI, self).setDefaults()

    def run(self):
        gtk.gdk.threads_enter()
        super(MainGUI, self).run()
        gtk.gdk.threads_leave()

    def onDeleteWindow(self, widget, data=None):
        print "starting new thread"
        threading.Thread(target=super(MainGUI, self).onDeleteWindow, args=(widget, data)).start()

    def btnEmailConnectClicked(self, widget, data=None):
        print "starting new thread"
        threading.Thread(target=super(MainGUI, self).btnEmailConnectClicked, args=(widget, data)).start()

    def btnCameraNetworkConnectClicked(self, widget, data=None):
        print "starting new thread"
        threading.Thread(target=super(MainGUI, self).btnCameraNetworkConnectClicked, args=(widget, data)).start()

    def btnUpdateClicked(self, widget, data=None):
        print "starting new thread"
        threading.Thread(target=super(MainGUI, self).btnUpdateClicked, args=(widget, data)).start()

    def cmbCameraTypeChanged(self, widget, data=None):
        print "starting new thread"
        threading.Thread(target=super(MainGUI, self).cmbCameraTypeChanged, args=(widget, data)).start()

    def cmbCameraLocalNumberChanged(self, widget, data=None):
        print "starting new thread"
        threading.Thread(target=super(MainGUI, self).cmbCameraLocalNumberChanged, args=(widget, data)).start()

    def pilImageToPixbuf(self, img):
        import numpy
        arr = numpy.array(img)
        pixbuf = gtk.gdk.pixbuf_new_from_array(arr, self.Gtk.gdk.COLORSPACE_RGB, 8)
        return pixbuf

def run():
    hwg = MainGUI()
    hwg.run()
    print "Done."

if __name__ == "__main__":
    run()
