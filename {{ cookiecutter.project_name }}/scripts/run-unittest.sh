#!/bin/bash
set -euo pipefail

pip3 install -r requirements/development.txt
make unittests
