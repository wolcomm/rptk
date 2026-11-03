{
  lib,
  python3Packages,
  bgpq3,
}:
let
  pkg = python3Packages.buildPythonPackage {
    pname = "rptk";
    version = "0.3.0";
    src = ./.;
    propagatedBuildInputs = with python3Packages; [
      jinja2
      pyyaml
      flask
      whichcraft
    ];
    nativeCheckInputs = with python3Packages; [
      pytestCheckHook
      pytest-cov
      # pytest-flake8
      flake8
      flake8-docstrings
      flake8-import-order
      pep8-naming
      jsonschema
    ];
    makeWrapperArgs = [
      "--prefix PATH : ${lib.makeBinPath [ bgpq3 ]}"
    ];
  };
in
pkg.overrideAttrs (old: {
  passthru.pythonEnv = pkg.pythonModule.withPackages (ps: [
    pkg
    ps.gunicorn
    ps.gevent
  ]);
})
