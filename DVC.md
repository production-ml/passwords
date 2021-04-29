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
