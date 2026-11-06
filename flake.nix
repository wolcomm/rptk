{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    { self, ... }@inputs:
    let
      inherit (inputs.nixpkgs) lib;
      supportedSystems = with inputs.flake-utils.lib.system; [ x86_64-linux ];
    in
    inputs.flake-utils.lib.eachSystem supportedSystems (
      system:
      let
        pkgs = import inputs.nixpkgs { inherit system; };
        supportedPythons = {
          default = pkgs.python3Packages;
          inherit (pkgs)
            python310Packages
            python311Packages
            ;
        };
      in
      rec {
        packages = lib.mapAttrs (
          _: python3Packages: pkgs.callPackage ./default.nix { inherit python3Packages; }
        ) supportedPythons;
        checks = packages;
      }
    );
}
