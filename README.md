# Auth Service

Auth Service for ROSA system.

Master status: ![](https://github.com/RSOA-WEITI-2020/PythonProjectTemplate/workflows/Tests/badge.svg?branch=master)  
Develop status: ![](https://github.com/RSOA-WEITI-2020/PythonProjectTemplate/workflows/Tests/badge.svg?branch=develop)

Keys included in `/keys` directory are for testing purposes only and should be changed before deploy!

To start app locally:

- run `poetry install`
- run `poetry shell`
- run `flask run`

## Available endpoints

### `/v1/register`

Params (`x-www-form-url-encoded`):

- `username`
- `password`
- `email`

### `/v1/login`

Params (`x-www-form-url-encoded`):

- `username`
- `password`

Response:

```json
{
  "authToken": "ey...",
  "refreshToken": "ey..."
}
```

### `/v1/refresh-token`

Headers:

- `Authorization: Bearer <refreshToken>`

Response:

```json
{
  "authToken": "ey...",
  "refreshToken": "ey..."
}
```

### `/v1/public-key`

```json
{
  "key": "<public key used for tokens signing>"
}
```
