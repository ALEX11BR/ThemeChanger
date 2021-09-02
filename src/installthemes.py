import glob
import os
import shutil
import tempfile
from pathlib import Path

from gi.repository import Gtk, GLib

from .archivefilefilter import ArchiveFileFilter

def showArchiveChooserDialog(message):
    dialog = Gtk.FileChooserDialog(
        action=Gtk.FileChooserAction.OPEN,
        title=message,
    )
    dialog.add_buttons(
        Gtk.STOCK_CANCEL,
        Gtk.ResponseType.CANCEL,
        Gtk.STOCK_OPEN,
        Gtk.ResponseType.OK,
    )
    dialog.add_filter(ArchiveFileFilter())

    response = dialog.run()
    filename = dialog.get_filename()
    dialog.destroy()

    if response == Gtk.ResponseType.OK:
        return filename
    else:
        return False

def showErrorDialog(message, err):
    dialog = Gtk.MessageDialog(
        flags=0,
        message_type=Gtk.MessageType.ERROR,
        buttons=Gtk.ButtonsType.OK,
        text=message
    )
    dialog.format_secondary_text(err)
    dialog.run()
    dialog.destroy()

def showSuccessDialog(filename, section):
    dialog = Gtk.MessageDialog(
        flags=0,
        message_type=Gtk.MessageType.INFO,
        buttons=Gtk.ButtonsType.OK,
        text=f"The theme(s) from the archive at '{filename}' has been successfully installed!"
    )
    dialog.format_secondary_text(f"You can now set them in the '{section}' tab.")
    dialog.run()
    dialog.destroy()

def installThemeArchive(kind, archivePath, destination, anchorFile, anchorLevels, lookupFunction):
    # We can't be sure that the theme archive has in its root folders which contain the actual theme files
    # To mitigate this possible problem, we don't directly extract the archive in the '.themes' or '.icons' dir, but we do this:

    # First, let's get the archive name, without extensions, then cut its file name at the first period
    # (the archive file might have multiple periods in its name from possibly being a .tar.xz and all the others); let's call it the themeName
    themeName = os.path.basename(archivePath).partition(".")[0]
    # Then, we create a tempdir somewhere on the user's cache to have it (presumably) on the same partition as the theme install destination
    try:
        with tempfile.TemporaryDirectory(dir=GLib.get_user_cache_dir()) as tempDirPath:
            # Let's have in this tempdir which will get a weird name a dir with the themeName; its path will be called safePath.
            # Maybe the archive has in its root dir straight up the actual theme files;
            # this will ensure that even in this situation these theme files will lie in a decently named dir to be picked up and installed later
            safePath = os.path.join(tempDirPath, themeName)
            os.mkdir(safePath)
            # In this safePath we'll extract the given archive.
            shutil.unpack_archive(archivePath, safePath)
            # Now let's look for all the anchorFile's in our safePath populated with the archive contents.
            # An anchorFile can be 'gtk-3.0/gtk.css' for widget themes, 'index.theme' for icon themes, or '*.kvconfig' for Kvantum themes.
            # In the first case, anchorLevels is 2, and in the other ones is 1.
            # We'll go up in the directory hierarchy by anchorLevels...
            hasMatchingFiles = False
            for matchingFile in glob.iglob(os.path.join(safePath, "**", anchorFile), recursive=True):
                # Let's make sure that the file obeys the validity standards (for icon themes this matters as widget themes have index.theme too)
                if lookupFunction(matchingFile):
                    hasMatchingFiles = True
                    matchingFolder = matchingFile
                    for i in range(anchorLevels):
                        matchingFolder = os.path.dirname(matchingFolder)
                    shutil.copytree(matchingFolder, os.path.join(destination, os.path.basename(matchingFolder)), symlinks=True)
                # ...and copy the dir we arrive in to the desired destination. I couldn't find an easy way to copy a dir into an existing one,
                # so we copy it in the desired destination in a folder called after the themeName
            # And we're done. If there's any error, we'll raise it to the caller to handle it.
            # For instance, if there is not a single matching file, that's an error
            if not hasMatchingFiles:
                raise Exception(f"The archive doesn't have any {kind} theme!")
    except Exception as err:
        raise err

def checkIconIndexFile(pathname):
    keyFile = GLib.KeyFile()
    keyFile.load_from_file(pathname, GLib.KeyFileFlags.NONE)
    return keyFile.has_group("Icon Theme")

def checkKvantumFile(pathname):
    path = Path(pathname)
    return os.path.basename(pathname).partition(".")[0] == os.path.basename(os.path.dirname(pathname))