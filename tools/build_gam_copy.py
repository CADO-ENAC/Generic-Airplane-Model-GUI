"""Compile gam_copy.py into binary extension modules and place them at the repository root.

The source file gam_copy.py is not tracked by git; only the compiled modules are committed:
  - gam_copy.cpXY-win_amd64.pyd               for local use on Windows (built with the Python running this script)
  - gam_copy.cpython-3XY-x86_64-linux-gnu.so  for Linux, e.g. Streamlit Community Cloud (built in Docker)

Python imports a compiled module in preference to gam_copy.py when both sit in the same folder,
so re-run this script after every change to gam_copy.py, otherwise the app keeps using the old binary.

Requirements:
  - Windows build: `pip install cython setuptools` and Microsoft C++ Build Tools
  - Linux build:   Docker Desktop running

Usage (from the repository root):
  python tools/build_gam_copy.py              # Windows + Linux
  python tools/build_gam_copy.py --no-linux   # Windows only
  python tools/build_gam_copy.py --no-local   # Linux only
"""
import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SOURCE = REPO / "gam_copy.py"
LINUX_IMAGE = "quay.io/pypa/manylinux_2_28_x86_64"
LINUX_PYTHONS = ["cp39", "cp310", "cp311", "cp312", "cp313", "cp314"]

SETUP_PY = '''
from setuptools import setup, Extension
from Cython.Build import cythonize
setup(ext_modules=cythonize([Extension("gam_copy", ["gam_copy.py"])],
      compiler_directives={"language_level": "3", "emit_code_comments": False}),
      script_args=["build_ext", "--inplace"])
'''

LINUX_SCRIPT = r'''#!/bin/bash
export CFLAGS="-O2 -g0"
build_one() {
  v=$1; PY=/opt/python/$v-$v/bin/python
  [ -x "$PY" ] || { echo "skip $v (not in image)"; return; }
  d=/tmp/b_$v; mkdir -p $d && cp /work/gam_copy.py /work/setup.py $d/ && cd $d
  if $PY -m pip install -q cython setuptools >/dev/null 2>&1 && $PY setup.py >build.log 2>&1; then
    strip --strip-unneeded gam_copy.*.so && cp gam_copy.*.so /work/out/ && echo "ok   $v"
  else
    echo "FAIL $v"; tail -5 build.log
  fi
}
for v in VERSIONS; do build_one $v & done
wait
'''


def build_local(work: Path) -> list[Path]:
    d = work / "local"
    d.mkdir()
    shutil.copy2(SOURCE, d / SOURCE.name)
    (d / "setup.py").write_text(SETUP_PY, encoding="utf-8")
    subprocess.run([sys.executable, "setup.py"], cwd=d, check=True, stdout=subprocess.DEVNULL)
    return [p for p in d.glob("gam_copy*") if p.suffix in (".pyd", ".so")]


def build_linux(work: Path) -> list[Path]:
    d = work / "linux"
    (d / "out").mkdir(parents=True)
    shutil.copy2(SOURCE, d / SOURCE.name)
    (d / "setup.py").write_text(SETUP_PY, encoding="utf-8")
    script = LINUX_SCRIPT.replace("VERSIONS", " ".join(LINUX_PYTHONS))
    (d / "build.sh").write_text(script, encoding="utf-8", newline="\n")
    subprocess.run(["docker", "run", "--rm", "-v", f"{d}:/work", LINUX_IMAGE, "bash", "/work/build.sh"], check=True)
    return sorted((d / "out").glob("gam_copy*.so"))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-local", action="store_true", help="skip the build for the Python running this script")
    ap.add_argument("--no-linux", action="store_true", help="skip the Linux builds in Docker")
    args = ap.parse_args()
    if not SOURCE.exists():
        sys.exit(f"Source not found: {SOURCE}")

    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        built = []
        if not args.no_local:
            built += build_local(work)
        if not args.no_linux:
            built += build_linux(work)
        if not built:
            sys.exit("Nothing was built.")

        # Replace previous binaries of the same kind, then copy the new ones to the repository root
        kinds = {f.suffix for f in built}
        for old in REPO.glob("gam_copy.*"):
            if old.suffix in kinds:
                old.unlink()
        for f in built:
            shutil.copy2(f, REPO / f.name)
            print("installed", f.name)

    leftover = [p for p in REPO.glob("gam_copy*.c")]
    if leftover:
        print("WARNING: generated C file(s) in the repository, delete them:", leftover)


if __name__ == "__main__":
    main()
