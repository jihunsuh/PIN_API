from db import db
import datetime


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    username = db.Column(db.String(80))
    password = db.Column(db.String(200))
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password
        self.createdAt = datetime.datetime.now()
        self.updatedAt = datetime.datetime.now()

    def json(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'password': self.password,
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
            if record in ['email', 'username', 'password']:
                setattr(self, record, data[record])
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def create_bulk(cls, user_datas):
        for user_data in user_datas:
            user = cls(**user_data)
            db.session.add(user)
        db.session.commit()
