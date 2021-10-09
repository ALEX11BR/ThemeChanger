with import <nixpkgs> {};
mkShell {
    buildInputs = [
        (import ./default.nix { inherit pkgs python3Packages; })
    ];
    shellHook = ''
        themechanger
        exit
    '';
}