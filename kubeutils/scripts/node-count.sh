#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: node-count.sh CLUSTER_NAME"
  exit 1
fi

gcloud container clusters describe $1 --format json | jq ".currentNodeCount"
