#!/usr/bin/env python3

import utils as u

print("============ MIRROR TEST ============")

def test_mirror_help():
    print("mirror help: ")
    u.run_subprocess(u.hangar, ['mirror', '-h'])

    print("mirror help: ")
    u.run_subprocess(u.hangar, ['mirror', '--help'])

# jobs 1
def test_mirror_jobs_1():
    print("mirror jobs 1: ")
    u.run_subprocess(u.hangar, args=['mirror', '-f', './data/mirror_test.txt', '--debug', '--repo-type=harbor'], timeout=300)
    u.check_failed('mirror-failed.txt')

# jobs less than 1
def test_mirror_jobs_lt_1():
    print("mirror jobs less than 1: ")
    u.run_subprocess(u.hangar, args=['mirror', '-f', './data/mirror_test.txt', '-j', '0', '--repo-type=harbor', '--debug'], timeout=300)
    u.check_failed('mirror-failed.txt')

# jobs 20
def test_mirror_jobs_20():
    print("mirror jobs 20: ")
    u.run_subprocess(u.hangar, ['mirror', '-f', './data/mirror_test.txt','-j', '20', '--debug', '--repo-type=harbor'], timeout=300)
    u.check_failed('mirror-failed.txt')

# jobs more than 20
def test_mirror_jobs_gt_20():
    print("mirror jobs more than 20: ")
    u.run_subprocess(u.hangar, args=['mirror', '-f', './data/mirror_test.txt', '-j', '100', '--debug'], timeout=300)
    u.check_failed('mirror-failed.txt')

def test_mirror_validate():
    print("mirror validate: ")
    u.run_subprocess(u.hangar, ['mirror-validate', '-f', './data/mirror_test.txt', '-j', '10'], timeout=300)
    u.check_failed('mirror-validate-failed.txt')
