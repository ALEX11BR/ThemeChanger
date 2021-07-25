# ThemeChanger
This app is a theme changing utility for Linux, BSDs, and whatnots.
It lets the user change GTK 2/3/4, icon and cursor themes, edit GTK CSS with live preview, and set some related options.
It also lets the user install icon and widget theme archives.

# Installation
## From source
Make sure you have installed PyGobject, Gtk3, GLib (for the app running), meson, ninja (for the installation process).

In the folder with the source (obtainable e.g. by running `git clone https://github.com/ALEX11BR/ThemeChanger`) run `meson build`, then `ninja -C build install`, and you're ready to go!

# TODOs
- In the themes list add an identifying image for each theme
- Add some sort of Kvantum support
- Add more options to set (see [further reference](https://developer.gnome.org/gtk3/stable/GtkSettings.html))
- Add a client for OCS-compatible websites like gnome-look.org, tailored for downloading (and automatically installing) themes (see [API reference]() and [a reference project](https://www.opencode.net/dfn2/pling-store-development))
- Use a cleaner CSS live preview method
- Clean the code overall
