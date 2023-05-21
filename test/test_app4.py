import unittest
from flask import Flask
from flask_testing import TestCase
from app import app, db, Candidate, Employer

class FlaskAppTestCase(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        return app

    def setUp(self):
        db.create_all()
        # Create sample data for testing
        candidate = Candidate(username='testuser', password='testpass', email='test@example.com')
        employer = Employer(username='testemployer', password='testpass', email='test@example.com')
        db.session.add(candidate)
        db.session.add(employer)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('home.html')

    def test_candidate_register_route(self):
        response = self.client.get('/candidate_register')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('candidate_register.html')

        # Test POST request
        data = {'username': 'newuser', 'password': 'newpass', 'email': 'new@example.com'}
        response = self.client.post('/candidate_register', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('candidate_login.html')
        self.assertIn(b'A Candidate Successfully registered', response.data)

    def test_candidate_login_route(self):
        response = self.client.get('/candidate_login')
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('candidate_login.html')

        # Test POST request with valid credentials
        data = {'username': 'testuser', 'password': 'testpass'}
        response = self.client.post('/candidate_login', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('candidate_dashboard.html')
        self.assertIn(b'A Candidate Successfully logged in', response.data)

        # Test POST request with invalid credentials
        data = {'username': 'invaliduser', 'password': 'invalidpass'}
        response = self.client.post('/candidate_login', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assert_template_used('candidate_login.html')
        self.assertIn(b'Invalid credentials', response.data)

    # Add more test cases for other routes and functionalities

if __name__ == '__main__':
    unittest.main()
