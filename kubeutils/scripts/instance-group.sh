#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: instance-group.sh CLUSTER_NAME"
  exit 1
fi

gcloud container clusters describe $1 --format json | jq  --raw-output '.instanceGroupUrls[0]' | rev | cut -d'/' -f 1 | rev

