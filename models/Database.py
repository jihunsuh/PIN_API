from . import DB, Board, Pin, User


def initialize():
    DB.connect()
    DB.create_tables([User, Board, Pin], safe=True)
    DB.close()