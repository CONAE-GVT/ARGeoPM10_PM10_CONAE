#!/bin/bash -e

PARAMS=""
while (( "$#" )); do
  case "$1" in
    -i|--image)
      IMAGE_NAME=$2
      shift 2
      ;;
    -t|--tag)
      DOCKER_IMAGE_TAG=$2
      shift 2
      ;;
    -h|--help)
      echo "Usage: './tools/build.sh --image <image name> --tag <tag name>'. Defaults are 'empatia:latest'"
      exit 0
      ;;
    --) # end argument parsing
      shift
      break
      ;;
    -*|--*=) # unsupported flags
      echo "Error: Unsupported flag $1" >&2
      exit 1
      ;;
    *) # preserve positional arguments
      PARAMS="$PARAMS $1"
      shift
      ;;
  esac
done
# set positional arguments in their proper place
eval set -- "$PARAMS"

IMAGE_NAME=${IMAGE_NAME:-"empatia"}
IMAGE_TAG=${DOCKER_IMAGE_TAG:-'dev'}

# Generate Git Revision to include it in the Docker Image
#git rev-parse HEAD > .revision
#git rev-parse --short HEAD > .revision_short

docker build -t "${IMAGE_NAME}:${IMAGE_TAG}" -f Dockerfile .