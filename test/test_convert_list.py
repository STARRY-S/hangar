#!/usr/bin/env python3

import utils as u
import os, glob, shutil

print("============ CONVERT-LIST TEST ============")

def test_convert_list_help():
    print("convert-list help: ")
    u.run_subprocess(u.hangar, ['convert-list', '-h'])

def test_convert_list():
    print("convert-list: ")
    u.run_subprocess(u.hangar,
        ['convert-list', '-i', './data/save_test.txt',
        '-o', './converted.txt', '-s', 'docker.io'])
    f = open('converted.txt', "r")
    cv = f.read()
    print(cv)
    os.remove('converted.txt')
