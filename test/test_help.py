#!/usr/bin/env python3

import utils as u

def test_help():
    u.run_subprocess(u.hangar, ['help'])
    u.run_subprocess(u.hangar, ['-h'])
    u.run_subprocess(u.hangar, ['--help'])
