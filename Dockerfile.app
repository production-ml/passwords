FROM python:3.8.5-buster
ARG PROJNAME=app
ENV PROJNAME=${PROJNAME}
RUN mkdir /${PROJNAME}
WORKDIR /${PROJNAME}

# python packages
RUN pip install pipenv
COPY Pipfile .
COPY Pipfile.lock .
COPY packages packages
RUN pipenv install --deploy --system

# fetching code and model
COPY . .
# TODO: we download the latest artifact and can't deploy any other version with CI/CD
# to improve, we could use a specific tag stored in a file or something else
# TODO: dvc should not be installed in the docker image, but in the building environment
# the other reason to do that is that the --build-arg credentials to remote storage
# could be exposed unintentionally
RUN dvc get . model

# set env vars
# heroku will supply PORT value, and you should supply it yourself when running
ENV FLASK_RUN_PORT=$PORT

# run the command
RUN useradd -m myuser
USER myuser
CMD ["python", "app/app.py"]
