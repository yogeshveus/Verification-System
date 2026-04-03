import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_FOLDER = os.path.join(BASE_DIR, "database")
os.makedirs(DB_FOLDER, exist_ok=True)

DATABASE = os.path.join(DB_FOLDER, "users.db")
TEST_DATABASE = os.path.join(DB_FOLDER, "test_users.db")

SECRET_KEY = "secret123"