{
  description = "SurfAgent";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs";

  outputs = { self, nixpkgs }:
    let
      pkgs = import nixpkgs {
        localSystem = "x86_64-linux";
        config.allowUnfree = true;
      };
    in {
      devShell.x86_64-linux = pkgs.mkShell { buildInputs = [ pkgs.poetry ]; };
    };
}
