# -*- coding: utf-8 -*-
from models.User import User
from models import Pin, Board, DB


# DB에 접속할 때 default Board를 자동으로 생성해주는 함수
def auto_create_default_board():
    try:
        if_board_exists = Board.select().where(Board.title == 'default').get()
    except Board.DoesNotExist:
        Board.create_board('default', 'default')


def initialize():
    DB.connect()
    DB.create_tables([User, Board, Pin], safe=True)
    auto_create_default_board()
    DB.close()
