FROM python:3.8.5-buster
ARG PROJNAME=app
ENV PROJNAME=${PROJNAME}
RUN mkdir /${PROJNAME}
WORKDIR /${PROJNAME}

# python packages
COPY Pipfile .
COPY Pipfile.lock .
RUN pip install pipenv
RUN pipenv install --deploy --system
# TODO: move dvc to Pipfile
RUN pip install dvc[all]

# fetching code and model
COPY . .
# TODO: use specific tag stored in a file
RUN dvc pull
# TODO: checkout only current files, we don't need the full cache
RUN rm -rf .dvc/cache

# set env vars
# heroku will supply PORT value, and you should supply it yourself when running
ENV FLASK_RUN_PORT=$PORT

# run the command
RUN useradd -m myuser
USER myuser
CMD ["python", "app/app.py"]
