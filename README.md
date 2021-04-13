# flask User management 
Simple Flask app for displaying player scores in game contest.

## Setup and running
First install all necessary python packages using requirements.txt


```bash
pip install -r requirements.txt
```
### Setup database
To setup database run setup_db.py script:
```bash
python setup_db.py
```

Run server:
```bash
python run.py
```

Navigate to url http://127.0.0.1:8080/ in browser.

* /users (GET) - Returns JSOn with users from database.
* /users/<user_id> (GET) - Returns JSOn with user identified by user_id.
* /products (GET) - Returns JSOn with products from database.
* /products/<product_id> (GET) - Returns JSOn with product identified by product_id.
* /products/images-list (GET) - Returns JSOn with product images.
