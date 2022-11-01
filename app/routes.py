from .models import Authors, Books
from flask import jsonify, abort, request, Flask
from . import app, db
from sqlalchemy.sql import text


@app.route("/")
def index():
    return 'Hello, GiG!'

#Authors endpoints
@app.route("/authors", methods=["GET"])
def get_authors():
    authors = Authors.query.all()
    return jsonify([author.to_json() for author in authors])

@app.route("/authors/<id>", methods=["GET"])
def get_author(id):
    author = Authors.query.get_or_404(id)
    return jsonify(author.to_json())

@app.route('/authors', methods=['POST'])
def create_author():
    if not request.json:
        abort(400)
    author_name = request.json.get('name')
    if not author_name:
        abort(400)
    author = Authors(name=author_name)
    db.session.add(author)
    db.session.commit()
    return jsonify(author.to_json()), 201

@app.route("/authors/<id>", methods=["DELETE"])
def delete_author(id):
    author = Authors.query.get_or_404(id)
    db.session.delete(author)
    db.session.commit()
    return jsonify({'result': True})

@app.route('/authors/<id>', methods=['PATCH'])
def update_author(id):
    if not request.json or not request.json.get('name'):
        abort(400)
    author = Authors.query.get_or_404(id)
    author.name = request.json.get('name', author.name)
    db.session.commit()
    return jsonify(author.to_json()), 201


#Books endpoints
@app.route("/books", methods=["GET"])
@app.route("/books/author/<author_id>", methods=["GET"])
def get_books(author_id=0):
    books = Books.query.all()
    if author_id != 0:
        books = db.session.query(Books).filter(Books.author_id == author_id).all()
    return jsonify([book.to_json() for book in books])

@app.route("/books/<id>", methods=["GET"])
def get_book(id):
    author = Authors.query.get_or_404(id)
    return jsonify(author.to_json())

@app.route('/books', methods=['POST'])
def create_book():
    if not request.json:
        abort(400)
    author_id = request.json.get('author_id')
    author = Authors.query.get(author_id)
    if author is None:
        return jsonify({'result': 'Author id doesn\'t exist'}), 400
    book_name = request.json.get('name')
    if not book_name:
        abort(400)
    book = Books(
        name=book_name,
        author_id=author_id
    )
    db.session.add(book)
    db.session.commit()
    return jsonify(book.to_json()), 201

@app.route("/books/<id>", methods=["DELETE"])
def delete_book(id):
    book = Books.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'result': True})

@app.route('/books/<id>', methods=['PATCH'])
def update_book(id):
    if not request.json:
        abort(400)
    book = Books.query.get_or_404(id)
    if request.json.get('name'):
        book.name = request.json.get('name', book.name)
    if request.json.get('author_id'):
        author_id = request.json.get('author_id')
        author = Authors.query.get(author_id)
        if author is None:
            return jsonify({'result': 'Author id doesn\'t exist'})
        book.author_id = request.json.get('author_id', book.author_id)
    db.session.commit()
    return jsonify(book.to_json()), 201


