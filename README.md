# ThemeChanger
![A screenshot of our lovely ThemeChanger](screenshot1.png)

This app is a theme changing utility for Linux, BSDs, and whatnots.
It lets the user change GTK 2/3/4, Kvantum, icon and cursor themes, edit GTK CSS with live preview, and set some related options.
It also lets the user install icon and widget theme archives.

## Features
- Set the GTK 3 theme, sync the GTK2, GTK4, Kvantum themes with it or choose another one for each of these toolkits
- Set the icon theme
- Set the cursor theme, and tweak the cursor's size
- Set various options like whether buttons have images or not
- Edit GTK CSS with instantaneous feedback of the changes made
- Install new widget or icon themes from archives available e.g. at https://gnome-look.org

# Installation
## Arch Linux & friends
Install the `themechanger-git` package from the AUR the way you like it. For instance, I like it this way:
```
yay -S themechanger-git
```
## From source
Make sure you have installed PyGobject, Gtk3, GLib (for the app running); headers thereof, meson, ninja (for the installation process).

In the folder with the source (obtainable e.g. by running `git clone https://github.com/ALEX11BR/ThemeChanger`) run `meson build`, then `ninja -C build install`, and you're ready to go!

# TODOs
- Add more advanced Kvantum support (e.g. handling of the Kvantum theme names, which oftentimes don't match the GTK theme names, or syncing some options)
- Add more options to set (see [further reference](https://developer.gnome.org/gtk3/stable/GtkSettings.html))
- Add theme remover
- Add a client for OCS-compatible websites like gnome-look.org, tailored for downloading (and automatically installing) themes (see [API reference]() and [a reference project](https://www.opencode.net/dfn2/pling-store-development))
- Use a cleaner CSS live preview method
- Clean the code overall
