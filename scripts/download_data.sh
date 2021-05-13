echo "Get data from kaggle"
mkdir -p data/raw
kaggle competitions download -c dmia-sport-2019-fall-intro -f train.csv -p data/raw/
kaggle competitions download -c dmia-sport-2019-fall-intro -f Xtest.csv -p data/raw/
