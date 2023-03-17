#!/bin/bash

set -euo pipefail

cd $(dirname $0)/../
WORKINGDIR="$(pwd)/"

source ./scripts/env.sh

# help
pytest -s test_help.py

# version
pytest -s test_version.py

# mirror
# Mirror images from
pytest -s test_mirror.py

# save
pytest -s test_save.py

# load
pytest -s test_load.py

# sync

# compress

# decompress

# convert-list
pytest -s test_convert_list.py

# generate-list
