from app import db

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String, nullable=False)
    # Adicione outros campos conforme necessário, como timestamp, usuário, etc.

    def __repr__(self):
        return '<Log %r>' % self.id
