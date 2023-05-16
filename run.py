from flask_apscheduler import APScheduler
from app import app
from setup_db import reset_database, seed_users, seed_products


scheduler = APScheduler()


def reset_db():
    print('Reset database')
    reset_database()
    seed_products()
    seed_users()


if __name__ == '__main__':
    scheduler.add_job(id='Reset DB Task', func=reset_db, trigger='interval', minutes=30)
    scheduler.start()
    app.run(host='localhost', port=8080)
