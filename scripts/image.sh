#!/bin/bash

set -euo pipefail

cd $(dirname $0)/../

REPO=${REPO:-'cnrancher'}
TAG=${TAG:-'latest'}
BUILDER='hangar'
TARGET_PLATFORMS='linux/arm64,linux/amd64'
BUILDX_OPTIONS=${BUILDX_OPTIONS:-''} # Set to '--push' to upload images

docker buildx ls | grep -q ${BUILDER} || \
    docker buildx create --name=${BUILDER} --platform=${TARGET_PLATFORMS}

echo "Start build hangar images"

docker buildx build -f package/Dockerfile \
    --builder ${BUILDER} \
    -t "${REPO}/hangar:${TAG}" \
    --platform=${TARGET_PLATFORMS} \
    --attest type=provenance,mode=max \
    ${BUILDX_OPTIONS} .

echo "Image: Done"
