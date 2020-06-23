# Auth Service

Auth Service for ROSA system.

Master status: ![](https://github.com/RSOA-WEITI-2020/PythonProjectTemplate/workflows/Tests/badge.svg?branch=master)  
Develop status: ![](https://github.com/RSOA-WEITI-2020/PythonProjectTemplate/workflows/Tests/badge.svg?branch=develop)

Keys included in `/keys` directory are for testing purposes only and should be changed before deploy!
Key pathcould be set during `docker build` by adding params:

- `--build-arg PUBLIC_KEY=<path_to_public_key> --build-arg PRIVATE_KEY=<path_to_private_key>`.

Key files can be generated with:

```shell
ssh-keygen -t rsa -b 4096 -m PEM -f jwtRS256.key
openssl rsa -in jwtRS256.key -pubout -outform PEM -out jwtRS256.key.pub
```

To start app locally:

- run `poetry install`
- run `poetry shell`
- run `cd app && python main.py`

To start app in docker container with separate database in another container:
- create docker network \
  `docker network create develop`
- run mysql server \
  `docker run -p 3306:3306 -e MYSQL_ROOT_HOST=% -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=user_db --network=develop --name user_database mysql/mysql-server`
- run built auth service image \
  `docker run -p 80:80 --network=develop auth_service`

## Available endpoints

### `/v1/register`

Used to register

Params (`x-www-form-url-encoded`):

- `email`
- `password`
- `first_name`
- `last_name`
- `address`

### `/v1/login`

Used to get accessToken from credentials

Params (`x-www-form-url-encoded`):

- `email`
- `password`

Response:

```json
{
  "accessToken": "ey...",
  "refreshToken": "ey..."
}
```

### `/v1/refresh-token`

Used to refresh accessToken

Headers:

- `Authorization: Bearer <refreshToken>`

Response:

```json
{
  "accessToken": "ey...",
  "refreshToken": "ey..."
}
```

### `/v1/public-key`

Gets public key for signature validation

```json
{
  "key": "<public key used for tokens signing>"
}
```

### `/v1/me`

Gets logged user data

Headers:

- `Authorization: Bearer <accessToken>`

```json
{
  "email": "<email>"
}
```
