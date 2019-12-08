FROM dgnest/node:6.10.0
MAINTAINER Luis Mayta <@slovacus>

COPY Gemfile /app/Gemfile
COPY package.json /app/package.json

WORKDIR /app

RUN npm install --global gulp \
    && npm install --global gulp-cli \
    && bundle install \
    && npm install

CMD ["gulp"]
