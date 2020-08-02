from db import db
import datetime


class PinModel(db.Model):
    __tablename__ = 'pins'

    id = db.Column(db.Integer, primary_key=True)
    img_url = db.Column(db.String(200))
    description = db.Column(db.String(200))
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id'),
                         nullable=False)
    board = db.relationship('BoardModel',
                            backref=db.backref('pins', lazy=True))
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)

    def __init__(self, img_url, description, board_id):
        self.img_url = img_url
        self.description = description
        self.board_id = board_id
        self.createdAt = datetime.datetime.now()
        self.updatedAt = datetime.datetime.now()

    def json(self):
        return {
            'id': self.id,
            'img_url': self.img_url,
            'description': self.description,
            'board_id': self.board_id,
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
            if record in ['img_url', 'description', 'board_id']:
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
