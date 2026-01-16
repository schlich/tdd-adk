{
  description = "TDD-ADK - Test-Driven Development with TDFlow methodology";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    uv2nix.url = "github:adisbladis/uv2nix";
    uv2nix.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
      uv2nix,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        
        # Python package set from uv2nix
        pythonSet = uv2nix.lib.${system}.loadPyproject {
          projectRoot = ./.;
        };
      in
      {
        # Python package with dependencies from uv
        packages.tdd-eval = pythonSet.mkVirtualEnv "tdd-eval-env" {
          tdd-eval = [ ];
        };

        packages.default = self.packages.${system}.tdd-eval;

        devShells.default = pkgs.mkShell {
          name = "tdd-adk";

          buildInputs = with pkgs; [
            # Python with uv
            uv
            python312

            # Version control
            jujutsu # jj - Git-compatible VCS used in this project

            # Diagramming
            d2 # D2 diagram renderer for .d2 files

            # Development tools
            prek # Rust-based pre-commit tool (https://prek.j178.dev/)
            just # Command runner
          ];

          shellHook = ''
            echo "🧪 TDD-ADK Development Environment"
            echo ""
            echo "Available tools:"
            echo "  uv    - Python package manager"
            echo "  jj    - Jujutsu version control"
            echo "  d2    - D2 diagram renderer"
            echo ""
            echo "Python setup:"
            echo "  uv sync              - Install dependencies"
            echo "  uv run pytest        - Run tests"
            echo "  uv run python -m tdd_eval.cli - Run CLI"
            echo ""
            echo "Render diagrams:"
            echo "  d2 tdd-dataflow.d2 tdd-dataflow.svg"
            echo "  d2 tdflow-architecture.d2 tdflow-architecture.svg"
          '';
        };

        # Package for rendering all diagrams
        packages.diagrams = pkgs.stdenv.mkDerivation {
          pname = "tdd-adk-diagrams";
          version = "0.1.0";

          src = ./.;

          nativeBuildInputs = [ pkgs.d2 ];

          buildPhase = ''
            mkdir -p $out
            for f in *.d2; do
              if [ -f "$f" ]; then
                name="''${f%.d2}"
                d2 "$f" "$out/$name.svg"
                echo "Rendered $f -> $name.svg"
              fi
            done
          '';

          installPhase = "true"; # Already installed in buildPhase
        };

        packages.default = self.packages.${system}.diagrams;
      }
    );
}
