import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

window = Gtk.Window(title="Hello World")
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()

#THIS IS A GIT TEST