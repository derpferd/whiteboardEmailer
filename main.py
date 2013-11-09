#try:
#	import gui
#except:
import gui2 as gui
print "Falling back to Gtk2"


def main():
	gui.run()

if __name__ == '__main__':
	main()
