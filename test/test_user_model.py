import unittest
from app import create_app, db
from app.models import User

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User(password='foo')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='foo')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password='foo')
        self.assertTrue(u.verify_password('foo'))
        self.assertFalse(u.verify_password('bar'))

    def test_password_salts_are_random(self):
        u = User(password='foo')
        u2 = User(password='foo')
        self.assertTrue(u.password_hash != u2.password_hash)
