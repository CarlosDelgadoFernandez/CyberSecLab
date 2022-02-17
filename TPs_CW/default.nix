with import <nixpkgs> {};

let
     pkgs = import (builtins.fetchGit {          
         name = "pinned-nixpkgs";                                                 
         url = "https://github.com/nixos/nixpkgs/";                       
         ref = "refs/heads/nixos-21.11";                     
         rev = "1bd4bbd49bef217a3d1adea43498270d6e779d65";                                           
     }) {
        #  crossSystem = (import <nixpkgs>).pkgsCross.avr.buildPackages.gcc;
     };                                                                           
in

let
  chipwhisperer_pkg = ps: ps.callPackage ./chipwhisperer.nix {};
  pythonEnv = pkgs.python39.withPackages (ps: [
    ps.matplotlib
    ps.tqdm
    ps.numpy
    (chipwhisperer_pkg ps)
  ]);
in

 # Make a new "derivation" that represents our shell
pkgs.pkgsCross.avr.mkShell {
  name = "dev-env";

  nativeBuildInputs = with pkgs; [
    pythonEnv
    bash
    libusb1
    julia-bin
    # jupyter
  ];

  # The packages in the `buildInputs` list will be added to the PATH in our shell
  buildInputs = [
    # avrlibc
  ];
}