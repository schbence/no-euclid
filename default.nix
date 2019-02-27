{ buildPythonPackage, pygame, pyopengl, numpy }:
buildPythonPackage rec {
  pname = "no-euclid";
  version = "0.0.0";
  src = ./.;
  doCheck = false;
  buildInputs = [ pygame pyopengl numpy ];
}
