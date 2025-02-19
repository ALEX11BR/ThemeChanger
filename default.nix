{ pkgs, python3Packages }:
python3Packages.buildPythonApplication rec {
    pname = "themechanger";
    version = "0.12.1";
    format = "other";
    src = ./.;
    nativeBuildInputs = with pkgs; [
        gobject-introspection
        meson
        ninja
        pkg-config
        wrapGAppsHook
        desktop-file-utils
        gtk3
    ];
    buildInputs = with pkgs; [
        glib
        gtk3
        mate.mate-settings-daemon
        python3
        gsettings-desktop-schemas
    ];
    propagatedBuildInputs = with python3Packages; [
        pygobject3
    ];
    postPatch = ''
        patchShebangs postinstall.py
    '';
}
