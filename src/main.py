import os
import sys

from gi.repository import Gtk, Gio, GLib

from .window import ThemechangerWindow

class Application(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='com.github.alex11br.themechanger',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = ThemechangerWindow(app=self)
        win.present()


def main(version):
    # Here we're making some dirs necessary to prevent some "file not found" errors when writing when saving
    os.makedirs(os.path.join(GLib.get_user_config_dir(), "gtk-3.0"), exist_ok=True)
    os.makedirs(os.path.join(GLib.get_user_config_dir(), "gtk-4.0"), exist_ok=True)
    os.makedirs(os.path.join(GLib.get_home_dir(), ".icons", "default"), exist_ok=True)

    app = Application()
    return app.run(sys.argv)
