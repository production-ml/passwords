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


```bash
(password-complexity) (py38) ➜  password-complexity git:(dvc) ✗ dvc stage add -n download_data \
          -d scripts/download_data.sh \
          -o data/raw \
          sh scripts/download_data.sh

ERROR: The output paths:
'data/raw'('download_data')
'data/raw/train.csv.zip'('data/raw/train.csv.zip.dvc')
overlap and are thus in the same tracked directory.
To keep reproducibility, outputs should be in separate tracked directories or tracked individually.
```

```
ERROR:  output 'package/lstm_model/resources' is already tracked by SCM (e.g. Git).
    You can remove it from Git, then add to DVC.
        To stop tracking from Git:
            git rm -r --cached 'package/lstm_model/resources'
            git commit -m "stop tracking package/lstm_model/resources"
```
