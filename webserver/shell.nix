# simple.nix
with (import <nixpkgs> {});
mkShell {
  packages = [
    python38
    python38Packages.pip
    pipenv
    postgresql_13
    openssl
  ];
}
