#!/bin/sh
echo "Get data from kaggle"
kaggle competitions download -c dmia-sport-2019-fall-intro -f train.csv -p data/raw/
kaggle competitions download -c dmia-sport-2019-fall-intro -f Xtest.csv -p data/raw/
echo "Running ML training pipeline"
PYTHONPATH=./package/ python scripts/train.py
echo "Listing the resulting files and folders"
ls -R .
