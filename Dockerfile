FROM tiangolo/uwsgi-nginx-flask:python3.8

ARG PRIVATE_KEY=./keys/jwtRS256.key
ARG PUBLIC_KEY=./keys/jwtRS256.key.pub

COPY ./app /app
ADD pyproject.toml /

COPY $PRIVATE_KEY ${WORKSPACE}/keys/jwtRS256.key
COPY $PUBLIC_KEY ${WORKSPACE}/keys/jwtRS256.key.pub

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
