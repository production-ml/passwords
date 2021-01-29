FROM python:3.8.5-buster
ARG PROJNAME=password-app
ENV PROJNAME=${PROJNAME}
RUN mkdir /${PROJNAME}
WORKDIR /${PROJNAME}

# python packages
COPY Pipfile .
COPY Pipfile.lock .
RUN pip install pipenv
RUN pipenv install --system

# finally
COPY . .
EXPOSE 5000
ENV FLASK_RUN_PORT=5000

# run the command
RUN useradd -m myuser
USER myuser
CMD ["python", "./app.py"]
