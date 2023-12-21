# Theatre API Service


API for taking tickets to theatre


## Initialize locally

1. Clone the repository:
```bash
git clone https://github.com/SevKrok/theatre-api-service.git
```
2. Navigate to the project directory:
```bash
cd theatre_api_service
```


3. Create a virtual environment:
```bash
python -m venv venv
```
4. Activate the virtual environment:

On macOS and Linux:
```bash
source venv/bin/activate
```
On Windows:
```bash
venv\Scripts\activate
```
5. Install project dependencies:
```bash
pip install -r requirements.txt
```
6. Copy .env.sample to .env (you must make it) and fill it with all required data.
7. Run database migrations:
```bash
python manage.py migrate
```
8. Optional: If you want to refill your database with some data, use:
```bash
python manage.py loaddata theatre_service_db_data.json
```


## Run with Docker
Docker should be installed.

+ pull docker container
``` 
docker pull kalmaron/theatre_api_service
```
+ run container
```
docker-compose build
docker-compose up
```

## Getting access
+ [Create user](http://127.0.0.1:8000/api/user/register/)
+ [Get access token](http://127.0.0.1:8000/api/user/token/)
+ [Theatre API](http://127.0.0.1:8000/api/theatre/)
+ [Look for documentation](http://127.0.0.1:8000/api/doc/swagger/)
+ [Admin panel](http://127.0.0.1:8000/api/admin/)

## Features
+ JWT Authentication
+ Email-Based Authentication
+ Admin panel
+ Pagination for all pages
+ Throttling Mechanism
+ API documentation
+ Upload image to Play
+ Filtering Plays by genres
+ Managing reservations and tickets
+ Implement a new permission class for reading without auth
