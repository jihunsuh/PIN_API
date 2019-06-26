from .User import User
from .Board import Board
from .Pin import Pin
from . import DB


def auto_create_default_board():
    try:
        if_board_exists = Board.select().where(Board.title == 'default').get()
    except Board.DoesNotExist:
        Board.create_board('default', 'default')


def initialize():
    DB.connect()
    DB.create_tables([User, Board, Pin])
    auto_create_default_board()
    DB.close()