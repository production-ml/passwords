FROM python:3.8-buster
ARG PROJNAME=password-app
ENV PROJNAME=${PROJNAME}
RUN mkdir /${PROJNAME}
WORKDIR /${PROJNAME}

# python packages
COPY requirements/dev/Pipfile .
COPY requirements/dev/Pipfile.lock .
RUN pip install pipenv
RUN pipenv lock -r > requirements.txt
RUN pip install --use-feature=2020-resolver --no-dependencies --no-cache-dir -r requirements.txt

# finally
COPY . .
EXPOSE 5000
ENV FLASK_RUN_PORT=5000

# run the command
CMD ["python", "./app.py"]
