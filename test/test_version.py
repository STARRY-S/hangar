#!/usr/bin/env python3

import utils as u

def test_version():
    u.run_subprocess(u.hangar, ['version'])
    u.run_subprocess(u.hangar, ['-v'])
    u.run_subprocess(u.hangar, ['--version'])
