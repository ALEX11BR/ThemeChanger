from shutil import get_unpack_formats

from gi.repository import Gtk

class ArchiveFileFilter(Gtk.FileFilter):
    def __init__(self):
        super().__init__()

        self.set_name("Supported archive formats")

        for formatTuple in get_unpack_formats():
            for supportedFormat in formatTuple[1]:
                self.add_pattern("*" + supportedFormat)