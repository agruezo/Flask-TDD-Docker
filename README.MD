[![CI/CD](https://github.com/agruezo/Flask-TDD-Docker/actions/workflows/main.yml/badge.svg)](https://github.com/agruezo/Flask-TDD-Docker/actions/workflows/main.yml)

<h3>ISSUES WITH MAC M1:</h3>

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

<h3>ALTERNATIVE WAYS TO DEPLOY WITH GITHUB ACTIONS USING A RELEASE.SH FILE:</h3>

- Add the following to a release.sh file in the root directory of your repo:
   - `HEROKU_REGISTRY_IMAGE`, `APP_NAME`, and `HEROKU_API_KEY` are environment variables

      ```
      #!/bin/sh

      set -e

      IMAGE_ID=$(docker inspect ${HEROKU_REGISTRY_IMAGE} --format={{.Id}})
      PAYLOAD='{"updates": [{"type": "web", "docker_image": "'"$IMAGE_ID"'"}]}'

      curl -n -X PATCH https://api.heroku.com/apps/$APP_NAME/formation \
         -d "${PAYLOAD}" \
         -H "Content-Type: application/json" \
         -H "Accept: application/vnd.heroku+json; version=3.docker-releases" \
         -H "Authorization: Bearer ${HEROKU_API_KEY}"

- Add the following to your yml file:

   ```
   run: | 
      chmod +x ./release.sh
      docker build -f ./Dockerfile.prod -t $HEROKU_REGISTRY_IMAGE .
      docker login -u _ -p $HEROKU_API_KEY registry.heroku.com
      docker push $HEROKU_REGISTRY_IMAGE
      ./release.sh