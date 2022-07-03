# dh-url-shortener
 
### Environtment

Create .env file and insert fields:
````
ENV_NAME="Development"
BASE_URL="http://127.0.0.1:800"
DB_URL="sqlite:///./url.db"
````
### Virtual environment

````
python -m virtualenv venv
python -m pip install -r requirements.txt
````

### Run project

Run project in DH-URL-SHORTENER folder with;
````
uvicorn app.main:app
````

## Endpoints

1. To healthcheck of microservice;
````
curl -X 'GET' \
  'http://localhost:8000/' \
  -H 'accept: application/json'
````
2. List of urls;
````
curl -X 'GET' \
  'http://localhost:8000/list' \
  -H 'accept: application/json'
````
3. To create url;
````
curl -X 'POST' \
  'http://localhost:8000/url' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "original_url": "www.example.com"
}'
````

``/url`` endpoint takes argument for original url and generate short url.
`
4. Redirect to original url by short url
 ````
 curl -X 'GET' \
  'http://localhost:8000/gczdib' \
  -H 'accept: application/json'
 ````
 
 ### Send get request to http://localhost:8000/{url_key}
 ### url_key is short url of original url. This endpoint redirects the original url. 