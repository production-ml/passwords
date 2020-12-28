FROM python:3.8-buster
ARG PROJNAME=password-app
ENV PROJNAME=${PROJNAME}
RUN mkdir /${PROJNAME}
WORKDIR /${PROJNAME}

# python packages
COPY requirements.txt .
RUN pip install --use-feature=2020-resolver --no-dependencies --no-cache-dir -r requirements.txt

# finally
COPY . .
EXPOSE 5000
ENV FLASK_RUN_PORT=5000

# run the command
CMD ["python", "./app.py"]
