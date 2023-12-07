from sqlalchemy import ForeignKey,DateTime
from app import db
from sqlalchemy.sql import func


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String, nullable=False)
    predicao = db.Column(db.Integer, nullable=False)
    date_time = db.Column(DateTime, default=func.now())
    # Adicione outros campos conforme necessário, como timestamp, usuário, etc.

    def __repr__(self):
        return '<Log %r>' % self.id
