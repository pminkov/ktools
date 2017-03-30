#!/bin/bash

gcloud container clusters describe $1 --format json | jq  --raw-output '.instanceGroupUrls[0]' | rev | cut -d'/' -f 1 | rev

