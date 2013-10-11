from gi.repository import Gtk
from gi.repository import GdkPixbuf
from cam import NetworkCamera
from emailer import Mailer
from PIL import Image
from StringIO import StringIO

class Handler:
	def __init__(self):
		self.bufferedPic = None
		self.emailer = None
		self.camera = None
		self.lblEmailStatus = builder.get_object("lblEmailStatus")
		self.txtEmailServer = builder.get_object("txtEmailServer")
		self.txtEmailPort = builder.get_object("txtEmailPort")
		self.txtEmailUsername = builder.get_object("txtEmailUsername")
		self.txtEmailPassword = builder.get_object("txtEmailPassword")
		self.swtEmailUseTLS = builder.get_object("swtEmailUseTLS")

	def onDeleteWindow(self, *args):
		Gtk.main_quit(*args)

	def btnUpdate(self, button):
		print "updating.."
		buff = StringIO()
		img = cam.getImage()
		self.bufferedPic = img
		img.thumbnail((320, 240), Image.ANTIALIAS)
		img.save(buff, "png")
		contents = buff.getvalue()
		buff.close()

		loader = GdkPixbuf.PixbufLoader.new_with_type('png')
		loader.write(contents)
		pixbuf = loader.get_pixbuf()
		loader.close()

		image = builder.get_object("image1")
		image.set_from_pixbuf(pixbuf)

	def btnSendEmail(self, button):
		if self.bufferedPic:
			buff = StringIO()
			self.bufferedPic.save(buff, format="jpeg")
			buffStr = buff.getvalue()
			buff.close()
			email.sendMail("beau0307@d.umn.edu", ["123.jonathan@gmail.com"], "test attachment", "test", [("test.jpg", buffStr)])
		else:
			print "No Image: Take an Image"

	def btnEmailConnect(self, button):
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
			self.lblEmailStatus.set_text("Connection with server failed.")
			self.emailer = None
			return

		try:
			self.emailer.tryLogin()
		except:
			self.lblEmailStatus.set_text("Login Failed.")
			self.emailer = None
			return

		self.lblEmailStatus.set_text("Connection .")


def run():
	builder = Gtk.Builder()
	builder.add_from_file("main.glade")
	builder.connect_signals(Handler())

	window = builder.get_object("windowMain")
	window.show_all()
	Gtk.main()
	print "Done."
