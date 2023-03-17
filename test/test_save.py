#!/usr/bin/env python3

import utils as u
import os, glob
import shutil

print("============ SAVE TEST ============")

def get_save_env():
    my_env = os.environ.copy()
    my_env["SOURCE_REGISTRY"] = my_env["DEST_REGISTRY"]
    my_env["SOURCE_USERNAME"] = my_env["DEST_USERNAME"]
    my_env["SOURCE_PASSWORD"] = my_env["DEST_PASSWORD"]
    my_env["DEST_REGISTRY"] = my_env["DEST_USERNAME"] = my_env["DEST_PASSWORD"] = ''
    return my_env

def test_save_help():
    print("save help: ")
    u.run_subprocess(u.hangar, ['save', '-h'])

# jobs 1
def test_save_jobs_1():
    print("save jobs 1: ")
    e = get_save_env()
    u.run_subprocess(u.hangar, args=['save', '-f', './data/save_test.txt', '--debug'], timeout=300, env=e)
    shutil.rmtree("saved-image-cache")
    u.check_failed('save-failed.txt')
    if not os.path.isfile('saved-images.tar.gz'):
        raise u.ProcessFailedException('failed')

# jobs less than 1
def test_save_jobs_lt_1():
    print("save jobs less than 1: ")
    e = get_save_env()
    u.run_subprocess(u.hangar, args=['save', '-f', './data/save_test.txt', '-j', '0', '--debug'], timeout=300, env=e)
    u.check_failed('save-failed.txt')
    shutil.rmtree("saved-image-cache")
    if not os.path.isfile('saved-images.tar.gz'):
        raise u.ProcessFailedException('failed')

# jobs 20
def test_save_jobs_20():
    print("save jobs 20: ")
    e = get_save_env()
    u.run_subprocess(u.hangar, ['save', '-f', './data/save_test.txt','-j', '20', '--debug'], timeout=300, env=e)
    shutil.rmtree("saved-image-cache")
    u.check_failed('save-failed.txt')
    if not os.path.isfile('saved-images.tar.gz'):
        raise u.ProcessFailedException('failed')

# jobs more than 20
def test_save_jobs_gt_20():
    print("save jobs more than 20: ")
    e = get_save_env()
    u.run_subprocess(u.hangar, args=['save', '-f', './data/save_test.txt', '-j', '100', '--debug'], timeout=300, env=e)
    shutil.rmtree("saved-image-cache")
    u.check_failed('save-failed.txt')
    if not os.path.isfile('saved-images.tar.gz'):
        raise u.ProcessFailedException('failed')

# zstd
def test_save_zstd():
    print("compress format zstd: ")
    os.remove('saved-images.tar.gz')
    e = get_save_env()
    u.run_subprocess(u.hangar,
                    args=['save', '-f', './data/save_test.txt', '-j', '10', '--compress', 'zstd', '--debug'],
                    timeout=300, env=e)
    shutil.rmtree("saved-image-cache")
    u.check_failed('save-failed.txt')
    if not os.path.isfile('saved-images.tar.zstd'):
        raise u.ProcessFailedException('failed')
    os.remove('saved-images.tar.zstd')

# compress=dir
def test_save_dir():
    print("compress format dir: ")
    e = get_save_env()
    u.run_subprocess(u.hangar,
                    args=['save', '-f', './data/save_test.txt', '-j', '10', '--compress', 'dir', '--debug'],
                    timeout=300, env=e)
    u.check_failed('save-failed.txt')
    if os.path.isfile('saved-images.tar.gz'):
        raise u.ProcessFailedException('failed')
    if not os.path.isdir('saved-images'):
        raise u.ProcessFailedException('failed')
    # shutil.rmtree("saved-images")

# segment compress (part size 100M)
def test_save_part():
    print("segment compress, part size 100M: ")
    e = get_save_env()
    u.run_subprocess(u.hangar,
                    args=['save', '-f', './data/save_test.txt', '-j', '10',
                          '--compress', 'gzip', '--part', '--part-size=100M', '--debug'],
                    timeout=300, env=e)
    shutil.rmtree("saved-image-cache")
    u.check_failed('save-failed.txt')
    saved_file_list = glob.glob('saved-images.tar.gz.part*')
    print('saved segment compress files:', saved_file_list)
    assert len(saved_file_list) != 0
    for i in saved_file_list:
        os.remove(i)
