from flask import request
from app import app, db, User, encrypt_word, decrypt_word
import unittest


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_users_not_duplicated(self):
        #create new user
        u = User(username='lex', score=5)
        db.session.add(u)
        db.session.commit()
        users = User.query.all()
        assert len(users) == 1


        with self.app as req:
            #test that existing user is not duplicated and score is updated
            req.get('/won?username=lex&level=4', follow_redirects = True)
            assert request.path == '/won'
            assert request.args.get('username') == 'lex'
            assert request.args.get('level') == '4'
            assert u.score == 9

            #Test that new user is added when user does not exist
            req.get('/won?username=lex1&level=3', follow_redirects = True)
            users = User.query.all()
            assert len(users) == 2


if __name__ == '__main__':
    unittest.main()