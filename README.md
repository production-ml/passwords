# Production service to predict password complexity

This is the production service to predict password complexity which was developed for the course about Production Machine Learning.

Python 3.8.5 is used.

## Notes

### git lfs

Note that `packages/app` is added as subtree: `git subtree add --prefix packages/app git@gitlab.com:production-ml/password_app.git master --squash`.
Unfortunately, git lfs doesn't support this subtree: https://github.com/git-lfs/git-lfs/issues/854.
The resolution is describe in one of the first commits in the page above: one need to cd to the subtree'd repo and then push files stored with lfs to the new repo. Running `git subtree add ...` after that will successfully fetch all lfs referenced data.

### git subtree

Updating subtree content is done via `git subtree pull --prefix packages/app git@gitlab.com:production-ml/password_app.git master --squash`

# Passwords_app

Flask-ML application to predict password frequency

## Installation

First clone the repo locally.
~~~bash
- $ git clone https://gitlab.com/production-ml/password_app
- $ cd password_app
~~~

Install Pipenv and its dependencies.
~~~bash
- $ pip install pipenv
~~~

Activate the virtual environment.
~~~bash
- $ pipenv shell
- $ pipenv install --dev
~~~

For deploy you should use commands:
~~~bash
- $ pipenv shell
- $ pipenv install
~~~

Run the web application via
~~~bash
- $ python app.py
~~~

Deactivate the virtual environment.
~~~bash
- $ exit
~~~

## Jupyter enviromnet settings:

Activate the virtual environment.
~~~bash
- $ pipenv shell
- $ pipenv install --dev
~~~

~~~bash
- $ python -m ipykernel install --user --name=venv38
~~~

## Launch jupyter:
~~~bash
- $ jupyter notebook
- select kernel "venv38"
~~~

## Development

To commit changes, first run `pre-commit install`. If you have no pre-commit installed, you can do it following instructiosn at https://pre-commit.com
