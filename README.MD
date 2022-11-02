[![CI/CD](https://github.com/agruezo/Flask-TDD-Docker/actions/workflows/main.yml/badge.svg)](https://github.com/agruezo/Flask-TDD-Docker/actions/workflows/main.yml)

Issues with Mac M1:

- Requirements.txt file:
   - can't include `psycopg2-binary == 2.9.3` due to libpq version 10 issue
   - instead include this as part of your dependencies in your Dockerfile:

      ```
      RUN apt update -y \
      && apt install -y build-essential libpq-dev

      RUN pip3 install psycopg2-binary --no-binary psycopg2-binary

- When building Dockerfile.prod:
   - run the following in the command line:

      ```
      docker build -f Dockerfile.prod  --platform linux/amd64 -t registry.heroku.com/APP_NAME/web .

Alternative way to deploy in GitHub actions using a .sh file
```
   run: | 
      chmod +x ./release.sh
      docker build -f ./Dockerfile.prod -t $HEROKU_REGISTRY_IMAGE .
      docker login -u _ -p $HEROKU_API_KEY registry.heroku.com
      docker push $HEROKU_REGISTRY_IMAGE
      ./release.sh