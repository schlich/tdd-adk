{
  description = "TDD-ADK - Test-Driven Development with TDFlow methodology";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default = pkgs.mkShell {
          name = "tdd-adk";

          buildInputs = with pkgs; [
            # Version control
            jujutsu # jj - Git-compatible VCS used in this project

            # Diagramming
            d2 # D2 diagram renderer for .d2 files

            # Development tools
            prek # Preview tool
            just # Command runner
          ];

          shellHook = ''
            echo "🧪 TDD-ADK Development Environment"
            echo ""
            echo "Available tools:"
            echo "  jj    - Jujutsu version control"
            echo "  d2    - D2 diagram renderer"
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
