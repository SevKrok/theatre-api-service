# Theatre API Service


API for taking tickets to theatre


## Initialize locally
Install PostgresSQL and create db.

1. Clone the repository:
```bash
git clone https://github.com/SevKrok/theatre-api-service.git
```
2. Navigate to the project directory:
```bash
cd theatre_api_service
```

3. Switch to the develop branch:
```bash
git checkout develop
```
4. Create a virtual environment:
```bash
python -m venv venv
```
5. Activate the virtual environment:

On macOS and Linux:
```bash
source venv/bin/activate
```
On Windows:
```bash
venv\Scripts\activate
```
6. Install project dependencies:
```bash
pip install -r requirements.txt
```
7. Copy .env.sample to .env (you must make it) and fill it with all required data.
8. Run database migrations:
```bash
python manage.py migrate
```
9. Optional: If you want to refill your database with some data, use:
```bash
python manage.py loaddata airport_db_data.json
```
10. Start the development server:
```bash
python manage.py runserver
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
* Create user: `/api/user/register/`
* Get access token: `/api/user/token/`
* Look for documentation: `/api/doc/swagger/`
* Admin panel: `/admin/`

## Features
* JWT Authentication
* Email-Based Authentication
* Admin panel
* Throttling Mechanism
* API documentation
* Upload image to Play
* Filtering Plays by genres
* Managing reservations and tickets
* Implement a new permission class for reading without auth
