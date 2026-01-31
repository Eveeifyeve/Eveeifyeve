{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
    git-hooks-nix.url = "github:cachix/git-hooks.nix";
    treefmt-nix.url = "github:numtide/treefmt-nix";
    systems.url = "github:nix-systems/default";
  };

  outputs =
    inputs@{
      self,
      flake-parts,
      nixpkgs,
      systems,
      ...
    }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = import systems;
      imports = [
        inputs.treefmt-nix.flakeModule
        inputs.git-hooks-nix.flakeModule
      ];

      flake.projectsList = [
        {
          owner = "Eveeifyeve";
          repo = "Dotfiles";
        }
        {
          owner = "NixOps4";
          repo = "NixOps4";
        }
        {
          owner = "nix-community";
          repo = "nix-user-chroot";
        }
        {
          owner = "nix-community";
          repo = "nurl";
        }
      ];

      perSystem =
        {
          pkgs,
          lib,
          ...
        }:
        {
          treefmt.config = {
            projectRootFile = "flake.nix";
            flakeCheck = true;
            programs = {
              nixfmt-rfc-style.enable = true;
              statix.enable = true;
              mdsh.enable = true;
            };
          };

          pre-commit.settings.hooks = {
            treefmt.enable = true;
          };

          packages =
            let
              inherit (pkgs.writers) writeNuBin lib;
              opensource = lib.mapAttrsToList (k: v: "- ${k}: ${v}") {
                Nixpkgs = "Windows Enablement and Packaging Team Member & Nim Packaging Team Member";
              };
            in
            {
              roles = writeNuBin "gen-roles" ''
                let roles = (http get https://eveeifyeve.pages.dev/api/roles | decode | from json)
                let business = ($roles | reduce -f {} {|it,acc| $acc | upsert $it.business ($it.name)} | items {|it| $"- ($it.0): ($it.1)"} | str join ",\n")
                let opensource = "${lib.concatStringsSep "\n" opensource}"
                print $"""### Businesses\n($business)\n\n### Opensource Projects\n($opensource)"""
              '';

              skillIcon = writeNuBin "gen-skills" ''
                let skills = (http get https://eveeifyeve.pages.dev/api/skillIcon | decode | from json | str join ",")
                print $" <p align=\"center\"><a href=\"https://github.com/LelouchFR/skill-icons\"><img src=\"https://go-skill-icons.vercel.app/api/icons?i=($skills)&perline=13\" /></a></p>"
              '';

              pin-tags = pkgs.writeNuBin "gen-pin-tags" ''
                ls profile/pin-*.svg
                  | get name
                  | each { |file|
                      let stem = ($file | path basename | str replace ".svg" "")
                      let parts = ($stem | str replace "pin-" "" | split row "-")
                      let owner = $parts.0
                      let repo = ($parts | skip 1 | str join "-")
                      "<a href=\"https://github.com/" + $owner + "/" + $repo + "\"><img src=\"" + $file + "\" height=\"150em\" width=\"412em\" align=\"center\" alt=\"" + $owner + "/" + $repo + "\" /></a>"
                  }
                  | str join "\n"
              '';
            };

          devShells.default = pkgs.mkShell {
            packages = [
              pkgs.mdsh
              (pkgs.python3.withPackages (python-pkgs: [
                python-pkgs.requests
              ]))
            ];
          };
        };
    };
}
