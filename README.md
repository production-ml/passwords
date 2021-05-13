# Production service to predict password complexity

This is the production service to predict password complexity which was developed for the course about Production Machine Learning.

Python 3.8.5 is used.

## Notes

See https://gitlab.com/production-ml/password_app for more examples of web apps which expose the ML model via REST API.

## Development

To commit changes, first run `pre-commit install`. If you have no pre-commit installed, you can do it following instructiosn at https://pre-commit.com

## Heroku

### build and test docker locally

```
docker build -t password_complexity -f Dockerfile.app .
docker run -p 5000:5000 -e PORT=5000 docker.io/library/password_complexity
```

### deploy via package
 <!-- install CLI via https://devcenter.heroku.com/articles/getting-started-with-python#set-up -->

```
heroku login
heroku create
heroku buildpacks:set heroku/python
git push heroku feature/heroku-deploy-example:main
heroku open
```

### deploy via docker
```
heroku container:login
heroku stack:set container
git push heroku feature/heroku-deploy-example:main
heroku open
```

```
heroku logs --tail
```
