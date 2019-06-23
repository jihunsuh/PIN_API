from models import Board, Database
from app import app

@app.before_first_request
def auto_create_default_board():
    try:
        if_board_exists = Board.select().where(Board.title == 'default').get()
    except Board.DoesNotExist:
        Board.create_board('default', 'default')


Database.initialize()