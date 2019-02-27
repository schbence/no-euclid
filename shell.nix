{ pkgs ? import <nixpkgs> {}, ...}:
pkgs.python27Packages.callPackage ./default.nix {}
