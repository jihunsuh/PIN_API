from db import db
import datetime


class BoardModel(db.Model):
    __tablename__ = 'boards'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    comment = db.Column(db.String(200), nullable=False)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)

    def __init__(self, title, comment):
        self.title = title
        self.comment = comment
        self.createdAt = datetime.datetime.now()
        self.updatedAt = datetime.datetime.now()

    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'comment': self.comment,
            'createdAt': str(self.createdAt),
            'updatedAt': str(self.updatedAt)
        }

    @classmethod
    def findOne(cls, **filter):
        return cls.query.filter_by(**filter).first()

    @classmethod
    def findAll(cls):
        return cls.query.all()

    def create(self):
        db.session.add(self)
        db.session.commit()

    def update(self, **data):
        for record in data:
            if record in ['title', 'comment']:
                setattr(self, record, data[record])
        setattr(self, 'updatedAt', datetime.datetime.now())
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def create_bulk(cls, board_datas):
        for board_data in board_datas:
            board = cls(**board_data)
            db.session.add(board)
        db.session.commit()
