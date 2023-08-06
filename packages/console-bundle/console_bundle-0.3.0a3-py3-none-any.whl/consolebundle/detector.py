import sys
import shutil
from pathlib import Path
from consolebundle import CommandRunner

def isRunningInConsole():
    def compareExecutables(p1: Path, p2: Path):
        return p1.parents[0] == p2.parents[0] and p1.stem == p2.stem

    return Path(sys.argv[0]) == Path(CommandRunner.__file__) or compareExecutables(Path(sys.argv[0]), Path(shutil.which('console')))
