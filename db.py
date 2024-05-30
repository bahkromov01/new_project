import psycopg2

conn = psycopg2.connect(
    database='project',
    user='postgres',
    password='1436',
    host='localhost',
    port=5432
)

cur = conn.cursor()

create_users_table = """
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    status VARCHAR(30) NOT NULL,
    login_try_count INT NOT NULL DEFAULT 0,
    last_login_attempt TIMESTAMP
);
"""

create_todos_table = """
CREATE TABLE todos (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    todo_type VARCHAR(15) NOT NULL,
    user_id INT REFERENCES users(id)
);
"""

def create_table():
    cur.execute(create_users_table)
    cur.execute(create_todos_table)
    conn.commit()

def migrate():
    insert_into_users = """
    INSERT INTO users (username, password, role, status, login_try_count, last_login_attempt) 
    VALUES ('admin', '123', 'SUPERADMIN', 'ACTIVE', 0, NULL);
    """
    cur.execute(insert_into_users)
    conn.commit()

def init():
    create_table()
    migrate()

if __name__ == '__main__':
    init()
