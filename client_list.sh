#!/usr/bin/env bash

cd $(dirname $0)/

set -e
source .venv/bin/activate
set -u

python client_list.py