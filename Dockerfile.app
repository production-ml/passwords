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

# finally
COPY . .
ENV FLASK_RUN_PORT=$PORT
ENV PYTHONPATH=package

# run the command
RUN useradd -m myuser
USER myuser
CMD ["python", "package/app.py"]
