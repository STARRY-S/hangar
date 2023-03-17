#!/usr/bin/env python3

import utils as u
import os, glob
import shutil

print("============ LOAD TEST ============")

def get_save_env():
    my_env = os.environ.copy()
    my_env["SOURCE_REGISTRY"] = my_env["DEST_REGISTRY"]
    my_env["SOURCE_USERNAME"] = my_env["DEST_USERNAME"]
    my_env["SOURCE_PASSWORD"] = my_env["DEST_PASSWORD"]
    my_env["DEST_REGISTRY"] = my_env["DEST_USERNAME"] = my_env["DEST_PASSWORD"] = ''
    return my_env

def prepare_load_file():
    load_file_list = glob.glob('load-part.tar.gz.part*')
    if len(load_file_list) == 0:
        print("prepare load part files: ")
        e = get_save_env()
        u.run_subprocess(u.hangar,
                        args=['save', '-f', './data/save_test.txt', '-j', '5',
                            '--compress', 'gzip', '--part', '--part-size=100M',
                            '-d', 'load-part'],
                        timeout=300, env=e)
        shutil.rmtree("saved-image-cache")
        u.check_failed('save-failed.txt')

    if not os.path.isfile('load.tar.gz'):
        print("prepare load tgz file: ")
        e = get_save_env()
        u.run_subprocess(u.hangar,
                        args=['save', '-f', './data/save_test.txt', '-j', '5',
                            '--compress', 'gzip',
                            '-d', 'load.tar.gz'],
                        timeout=300, env=e)
        shutil.rmtree("saved-image-cache")
        u.check_failed('save-failed.txt')

    if not os.path.isfile('load.tar.zstd'):
        print("prepare load tzstd file: ")
        e = get_save_env()
        u.run_subprocess(u.hangar,
                        args=['save', '-f', './data/save_test.txt', '-j', '5',
                            '--compress', 'zstd',
                            '-d', 'load'],
                        timeout=300, env=e)
        shutil.rmtree("saved-image-cache")
        u.check_failed('save-failed.txt')

    if not os.path.isdir('load-directory'):
        print("prepare load dir: ")
        e = get_save_env()
        u.run_subprocess(u.hangar,
                        args=['save', '-f', './data/save_test.txt', '-j', '5',
                            '--compress', 'dir',
                            '-d', 'load-directory'],
                        timeout=300, env=e)
        u.check_failed('save-failed.txt')

def test_load_help():
    print("load help: ")
    u.run_subprocess(u.hangar, ['load', '-h'])

# jobs 1
def test_load_jobs_1():
    print("load jobs 1: ")
    prepare_load_file()
    print("start load jobs 1: ")
    u.run_subprocess(u.hangar,
                    args=['load', '-s', 'load.tar.gz', '-j', '10', '--compress', 'gzip'],
                    timeout=300)
    shutil.rmtree("saved-image-cache")
    u.check_failed('load-failed.txt')

# jobs 20
def test_load_jobs_20():
    print("load jobs 20: ")
    prepare_load_file()
    print("start load jobs 20: ")
    u.run_subprocess(u.hangar,
                    args=['load', '-s', 'load.tar.gz', '-j', '20', '--compress', 'gzip'],
                    timeout=300)
    shutil.rmtree("saved-image-cache")
    u.check_failed('load-failed.txt')

# load dir
def test_load_dir():
    print("load dir: ")
    prepare_load_file()
    print("start load dir: ")
    u.run_subprocess(u.hangar,
                    args=['load', '-s', 'load-directory', '-j', '10', '--compress', 'dir'],
                    timeout=300)
    shutil.rmtree("saved-image-cache")
    u.check_failed('load-failed.txt')

# load zstd
def test_load_zstd():
    print("load zstd: ")
    prepare_load_file()
    print("start load zstd: ")
    u.run_subprocess(u.hangar,
                    args=['load', '-s', 'load.tar.zstd', '-j', '10', '--compress', 'zstd'],
                    timeout=300)
    shutil.rmtree("saved-image-cache")
    u.check_failed('load-failed.txt')

# load part
def test_load_part():
    print("load part: ")
    prepare_load_file()
    print("start load part: ")
    u.run_subprocess(u.hangar,
                    args=['load', '-s', 'load-part.tar.gz.part0', '-j', '10', '--compress', 'gzip'],
                    timeout=300)
    shutil.rmtree("saved-image-cache")
    u.check_failed('load-failed.txt')

def test_load_validate():
    print("load validate gzip: ")
    u.run_subprocess(u.hangar, ['load-validate', '-s', './load.tar.gz', '-j', '10'], timeout=300)
    shutil.rmtree("saved-image-cache")
    u.check_failed('load-validate-failed.txt')

def test_load_validate_dir():
    print("load validate dir: ")
    u.run_subprocess(u.hangar, ['load-validate', '-s', './load-directory', '-j', '10', '--compress=dir'], timeout=300)
    u.check_failed('load-validate-failed.txt')
