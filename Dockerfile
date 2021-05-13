FROM python:3.8.5-buster
ARG PROJNAME=ml-pipeline
ENV PROJNAME=${PROJNAME}
RUN mkdir /${PROJNAME}
WORKDIR /${PROJNAME}

# install Node and CML
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash
RUN apt-get update
RUN apt-get install -y nodejs
RUN npm i -g @dvcorg/cml
# RUN apt-get install -y libcairo2-dev libpango1.0-dev libjpeg-dev libgif-dev \
#           librsvg2-dev libfontconfig-dev
# RUN npm install -g vega-cli vega-lite

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
