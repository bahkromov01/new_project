from db import cur, conn
from models import User, UserRole, UserStatus
from sessions import Session
import utils
from datetime import datetime, timedelta

session = Session()

LOCKOUT_PERIOD = timedelta(minutes=15)


def is_locked_out(username: str) -> bool:
    check_lockout_query = """
        SELECT login_try_count, last_login_attempt
        FROM users
        WHERE username = %s;
    """
    cur.execute(check_lockout_query, (username,))
    result = cur.fetchone()
    if result:
        login_try_count, last_login_attempt = result
        if login_try_count >= 3:
            lockout_end_time = last_login_attempt + LOCKOUT_PERIOD
            if datetime.now() < lockout_end_time:
                return True
            else:
                reset_attempts_query = """
                    UPDATE users
                    SET login_try_count = 0, last_login_attempt = %s
                    WHERE username = %s;
                """
                cur.execute(reset_attempts_query, (datetime.now(), username))
                conn.commit()
    return False


def login(username: str, password: str):
    user_session = session.check_session()
    if user_session:
        return utils.BadRequest('You are already logged in', status_code=401)

    if is_locked_out(username):
        return utils.BadRequest('Account is locked. Try again later', status_code=403)

    get_user_by_username = '''SELECT * FROM users WHERE username = %s;'''
    cur.execute(get_user_by_username, (username,))
    user_data = cur.fetchone()

    if not user_data:
        print(utils.BadRequest('Username not found in the database'))

    _user = User(
        username=user_data[1],
        password=user_data[2],
        user_id=user_data[0],
        role=UserRole(user_data[3]),
        status=UserStatus(user_data[4]),
        login_try_count=user_data[5]
    )

    if password != _user.password:
        update_count_query = """
            UPDATE users
            SET login_try_count = login_try_count + 1, last_login_attempt = %s
            WHERE username = %s;
        """
        cur.execute(update_count_query, (datetime.now(), _user.username))
        conn.commit()
        if _user.login_try_count + 1 >= 3:
            return utils.BadRequest('Account is locked. Try again later', status_code=403)
        return utils.BadRequest('Incorrect password')

    reset_attempts_query = """
        UPDATE users
        SET login_try_count = 0, last_login_attempt = %s
        WHERE username = %s;
    """
    cur.execute(reset_attempts_query, (datetime.now(), _user.username))
    conn.commit()

    session.add_session(_user)
    return print(utils.ResponseData(('User successfully logged in')))


if __name__ == '__main__':
    while True:
        choice = input('Enter your choice: ')
        if choice == '1':
            username = input('Enter your username: ')
            password = input('Enter your password: ')
            login(username, password)
        else:
            break
