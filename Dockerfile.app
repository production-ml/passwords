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

# set env vars
# heroku will supply PORT value, and you should supply it yourself when running
ENV FLASK_RUN_PORT=$PORT

# run the command
RUN useradd -m myuser
USER myuser
CMD ["python", "app/app.py"]
