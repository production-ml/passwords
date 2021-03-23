FROM python:3.8.5-buster
ARG PROJNAME=ml-pipeline
ENV PROJNAME=${PROJNAME}
RUN mkdir /${PROJNAME}
WORKDIR /${PROJNAME}

# python packages
COPY Pipfile .
COPY Pipfile.lock .
RUN pip install pipenv
RUN pipenv install --dev --system

# finally
COPY . .

# args
ARG KAGGLE_USERNAME=myusername
ENV KAGGLE_USERNAME=${KAGGLE_USERNAME}
ARG KAGGLE_KEY=mykey
ENV KAGGLE_KEY=${KAGGLE_KEY}

# run the command
CMD ["sh", "-ux", "./scripts/run_pipeline.sh"]
