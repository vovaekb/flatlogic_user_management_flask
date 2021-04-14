# flask User management 
Simple Flask app for displaying player scores in game contest.

## Setup and running
First install all necessary python packages using requirements.txt


```bash
pip install -r requirements.txt
```
### Setup database
User Management backend using PostgreSQL DBMS on default.
First you need to create database called 'user_management'. Default PostgreSQL user/password is postgres/123. You can change database name and user credentials in file app/database.py in line
```bash
SQLALCHEMY_DATABASE_URI = "postgres://postgres:123@localhost/user_management"
```

Set environment variable for Development mode:
```bash
export FLASK_DEV=true
```

To setup database run setup_db.py script:
```bash
python setup_db.py
```
This script will create all necessary tables in database for data model defined in app/models.py.

Run server:
```bash
python run.py
```
This script will run Flask script on port 8080.

Navigate to url http://127.0.0.1:8080/ in browser.

* /users (GET) - Returns JSOn with users from database.
* /users/<user_id> (GET) - Returns JSOn with user identified by user_id.
* /products (GET) - Returns JSOn with products from database.
* /products/<product_id> (GET) - Returns JSOn with product identified by product_id.
* /products/images-list (GET) - Returns JSOn with product images.
