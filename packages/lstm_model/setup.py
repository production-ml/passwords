"""
Read for explanation:
https://pipenv.pypa.io/en/latest/advanced/#pipfile-vs-setup-py
https://github.com/pypa/pipenv/issues/209
"""
from setuptools import find_packages, setup

setup(
    name="lstm_model",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "sklearn",
        "keras",
        "tensorflow-cpu",
        "loguru",
    ],
    version="0.1.0",
    description="LSTM model to predict password complexity",
    author="Vitaly Belov",
)
