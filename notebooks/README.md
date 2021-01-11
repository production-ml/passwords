## Settings:

Activate the virtual environment.
~~~bash
- $ cd requirements/jupyter/
- $ pipenv shell
- $ pipenv install
~~~

~~~bash
- $ python -m ipykernel install --user --name=venv38
~~~

## Launch jupyter:
~~~bash
- $ cd ../../
- $ jupyter notebook
- select kernel "venv38"
~~~

