{
  description = "SurfAgent";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs";

  outputs = { self, nixpkgs }:
    let
      pkgs = import nixpkgs {
        localSystem = "x86_64-linux";
        config.allowUnfree = true;
      };

      # The haskell package set override
      haskellExtend = hpFinal: hpPrev: {
        SurfAgent =
          hpPrev.callCabal2nix "SurfAgent" self { };
      };
      hsPkgs = pkgs.haskellPackages.extend haskellExtend;

      ciTools = [
        pkgs.cabal-install
        pkgs.haskellPackages.fourmolu
        pkgs.hlint
      ];
      devTools = [
        pkgs.haskell-language-server
        pkgs.ghcid
        pkgs.haskellPackages.cabal-fmt
        pkgs.just
      ];
    in {
      devShell.x86_64-linux = hsPkgs.shellFor {
        packages = p: [
          p.SurfAgent
        ];
        buildInputs = ciTools ++ devTools;
      };
    };
}
