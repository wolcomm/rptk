{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    { self, ... }@inputs:
    let
      supportedSystems = with inputs.flake-utils.lib.system; [ x86_64-linux ];
    in
    inputs.flake-utils.lib.eachSystem supportedSystems (
      system:
      let
        pkgs = import inputs.nixpkgs { inherit system; };
      in
      {
        packages.default = pkgs.callPackage ./default.nix { };
      }
    );
}
