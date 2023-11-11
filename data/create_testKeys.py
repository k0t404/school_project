#  этот файл в будущем может быть удален

from data import db_session
from data.keys import Keys


def create_keys():
    db_session.global_init('../db/logs.db')
    db_sess = db_session.create_session()
    key = Keys()
    key.key_available = '1111111'
    key.for_who = 'учитель'

    db_sess.add(key)

    key = Keys()
    key.key_available = '111111111'
    key.for_who = 'завуч'

    db_sess.add(key)

    key = Keys()
    key.key_available = '222222222'
    key.for_who = 'завуч'

    db_sess.add(key)

    db_sess.commit()
