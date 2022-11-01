from . import db

class Authors(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    books = db.relationship('Books', backref='authors')

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Books(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    author_id = db.Column(db.String(100), db.ForeignKey('authors.id', ondelete="CASCADE"), nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'author_id': self.author_id
        }