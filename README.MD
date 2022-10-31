Issues with Mac M1:

Requirements.txt file:
- can't include `psycopg2-binary == 2.9.3` due to libpq version 10 issue
- instead include this as part of your dependencies in your Dockerfile:
   - `RUN apt update -y \ `
    `&& apt install -y build-essential libpq-dev`

   - `RUN pip3 install psycopg2-binary --no-binary psycopg2-binary`

When building Dockerfile.prod:
- run the following in the command line:
    - `docker build -f Dockerfile.prod  --platform linux/amd64 -t registry.heroku.com/APP_NAME/web .`