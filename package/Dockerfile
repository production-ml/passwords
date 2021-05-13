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
RUN dvc checkout
# TODO: checkout only current files, we don't need the full cache
RUN rm -rf .dvc/cache

# finally
# COPY package .
# COPY config.toml .
EXPOSE 5000
ENV FLASK_RUN_PORT=5000
ENV PYTHONPATH=package

# run the command
RUN useradd -m myuser
USER myuser
CMD ["python", "package/app.py"]
