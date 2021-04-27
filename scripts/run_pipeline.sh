#!/bin/sh
echo "Download data"
sh download_data.sh
echo "Running ML training pipeline"
PYTHONPATH=./package/ python scripts/train.py
echo "Listing the resulting files and folders"
ls -R .
