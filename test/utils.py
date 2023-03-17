#!/usr/bin/env python3

# Run 'hangar version'

import subprocess, platform, glob, logging, sys, os

logging.basicConfig(format='%(asctime)s %(levelname)s: \n%(message)s', level=logging.INFO)

class ProcessFailedException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

def get_hangar_path(version):
    if platform.system() == "Darwin":
        system = "darwin"
    elif platform.system() == "Linux":
        system = "linux"
    else:
        print("unrecognized system: " + platform.system())
        return ""

    if platform.machine() == "arm64":
        arch = "arm64"
    elif platform.machine() == "aarch64":
        arch = "arm64"
    elif platform.machine() == "x86_64":
        arch = "amd64"
    else:
        print("unrecognized arch: " + platform.machine())
        return ""

    logging.debug("system: " + system)
    logging.debug("arch: " + arch)
    match = '../build/hangar-' + system + '-' + arch + '-' + version
    matchList = glob.glob(match)
    if not isinstance(matchList, list) or len(matchList) == 0:
        return ""
    return matchList[0]

# Run the subprocess and return its stdout, stderr, return code
def run_subprocess(path, args, timeout=10, stdin=None, stdout=None, stderr=None, env=None):
    logging.debug("run: " + path)
    args.insert(0, path)
    if stdin is None:
        stdin = sys.stdin
    if stdout is None:
        stdout = sys.stdout
    if stderr is None:
        stderr = sys.stderr

    # Launch the program using subprocess
    process = subprocess.Popen(
        args,
        stdin = stdin,
        stdout = stdout,
        stderr = stderr,
        text=True,
        env=env)
    # Wait for the program to finish
    ret = process.wait(timeout=timeout)
    if ret != 0:
        raise ProcessFailedException("subprocess failed")
    return ret

def check_failed(p):
    if os.path.exists(p):
        f = open(p, "r")
        raise ProcessFailedException(p + ':\n' + f.read())

hangar = get_hangar_path("*")
if hangar == "":
    print("failed to get hangar path")
    exit(1)
