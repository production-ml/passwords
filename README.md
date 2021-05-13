# Production service to predict password complexity

This is the production service to predict password complexity which was developed for the course about Production Machine Learning.

Python 3.8.5 is used.

## Notes

See https://gitlab.com/production-ml/password_app for more examples of web apps which expose the ML model via REST API.

## Development

To commit changes, first run `pre-commit install`. If you have no pre-commit installed, you can do it following instructiosn at https://pre-commit.com

## DVC

```
dvc stage add -n download_data \
          -d scripts/download_data.sh \
          -o data/raw \
          sh scripts/download_data.sh


dvc stage add -n process_data \
          -d scripts/process_data.py -d data/raw/train.csv.zip -d data/raw/Xtest.csv.zip \
          -o data/processed \
          python scripts/process_data.py data/raw/train.csv.zip data/raw/Xtest.csv.zip data/processed/


dvc stage add -n train_model --force \
          -d scripts/train.py -d data/processed \
          -o model \
          -p config.toml:model.embedding_dim,model.hidden_dim \
          --metrics-no-cache metrics.json \
          PYTHONPATH=./package/ python scripts/train.py data/processed model
```

To add service account key to Google Storage remote:
```
dvc remote modify gcs credentialpath focus-pottery-308512-6e19939465d6.json
```
