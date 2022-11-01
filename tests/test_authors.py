from app.routes import app, db
from app.models import Authors
import pytest
from config import config

app.config.from_object(config['testing'])
db.init_app(app)

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def setUp():
    with app.app_context():
        db.create_all()
        author1 = Authors(name='author 1')
        author2 = Authors(name='author 2')
        author3 = Authors(name='author 3')
        db.session.add(author1)
        db.session.add(author2)
        db.session.add(author3)
        db.session.commit()
        yield
        db.drop_all()

def test_get_all_authors(client,setUp):
    response = client.get('/authors')
    assert response.status_code == 200
    assert response.json == [{'id': 1, 'name': 'author 1'}, {'id': 2, 'name': 'author 2'}, {'id': 3, 'name': 'author 3'}]

def test_get_one_author(client,setUp):
    response = client.get('/authors/1')
    assert response.status_code == 200
    assert response.json == {'id': 1, 'name': 'author 1'}

def test_post_author_success_correct_payload(client,setUp):
    response = client.post('/authors', json= {'name': 'author 4'})
    assert response.status_code == 201
    authors = Authors.query.all()
    assert len(authors) == 4

def test_post_author_fail_wrong_payload(client,setUp):
    response = client.post('/authors', json={'some key': 'some value'})
    assert response.status_code != 201
    authors = Authors.query.all()
    assert len(authors) == 3

def test_delete_author_success(client,setUp):
    response = client.delete('/authors/1')
    assert response.status_code == 200
    authors = Authors.query.all()
    assert len(authors) == 2

def test_patch_author_success_correct_payload(client,setUp):
    response = client.patch('/authors/1', json={'name': 'author 1 updated'})
    assert response.status_code == 201
    author_name = Authors.query.get(1)
    assert author_name.name == 'author 1 updated'

def test_patch_author_fail_wrong_payload(client,setUp):
    response = client.patch('/authors/1', json={'some key': 'some value'})
    assert response.status_code != 201
