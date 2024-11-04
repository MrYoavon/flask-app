from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # define database


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=func.now())


def __repr__(self):
        return '<Task %r>' % self.id
