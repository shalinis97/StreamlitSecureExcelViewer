# tests/test_auth.py

import unittest
from auth import hash_password, verify_password
from database.database_setup import User, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import bcrypt
import os

class TestAuthentication(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up a test database
        cls.engine = create_engine('sqlite:///database/test_users.db')
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()

        # Add a test user
        cls.test_user = User(
            full_name='Test User',
            email='test@subasolutions.com',
            username='testuser',
            password=hash_password('Test@123'),
            is_admin=False,
            must_change_password=True
        )
        cls.session.add(cls.test_user)
        cls.session.commit()

    @classmethod
    def tearDownClass(cls):
        cls.session.close()
        os.remove('database/test_users.db')

    def test_password_hashing(self):
        plain_password = 'SecurePass@1'
        hashed = hash_password(plain_password)
        self.assertTrue(verify_password(plain_password, hashed))
        self.assertFalse(verify_password('WrongPass', hashed))

    def test_user_login(self):
        user = self.session.query(User).filter(User.username == 'testuser').first()
        self.assertIsNotNone(user)
        self.assertTrue(verify_password('Test@123', user.password))
        self.assertFalse(verify_password('Incorrect', user.password))

if __name__ == '__main__':
    unittest.main()
