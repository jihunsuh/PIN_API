from models.user import User
# from models.board import Board
from models.pin import Pin
from models import DB


# def auto_create_default_board():
#     try:
#         Board.select().where(Board.title == 'default').get()
#     except Board.DoesNotExist:
#         Board.create_board('default', 'default')


# def initialize():
#     DB.connect()
#     DB.create_tables([User, Board, Pin])
#     auto_create_default_board()
#     DB.close()
