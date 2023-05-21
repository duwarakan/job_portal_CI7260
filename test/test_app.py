import unittest
from flask_testing import TestCase
from flask import session
from app import app, db, Candidate, Employer, CV


class TestApp(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_candidate_register(self):
        response = self.client.post('/candidate_register', data=dict(username='test_candidate', password='password', email='test_candidate@example.com'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Candidate Login', response.data)

    def test_candidate_login(self):
        candidate = Candidate(username='test_candidate', password='password', email='test_candidate@example.com')
        db.session.add(candidate)
        db.session.commit()
        response = self.client.post('/candidate_login', data=dict(username='test_candidate', password='password'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Candidate Dashboard', response.data)

    def test_employer_register(self):
        response = self.client.post('/employer_register', data=dict(username='test_employer', password='password', email='test_employer@example.com'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Employer Login', response.data)

    def test_employer_login(self):
        employer = Employer(username='test_employer', password='password', email='test_employer@example.com')
        db.session.add(employer)
        db.session.commit()
        response = self.client.post('/employer_login', data=dict(username='test_employer', password='password'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Employer Dashboard', response.data)

    def test_candidate_dashboard_access(self):
        candidate = Candidate(username='test_candidate', password='password', email='test_candidate@example.com')
        db.session.add(candidate)
        db.session.commit()
        with self.client.session_transaction() as sess:
            sess['candidate_id'] = candidate.id
        response = self.client.get('/candidate_dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Candidate Dashboard', response.data)

    def test_employer_dashboard_access(self):
        employer = Employer(username='test_employer', password='password', email='test_employer@example.com')
        db.session.add(employer)
        db.session.commit()
        with self.client.session_transaction() as sess:
            sess['employer_id'] = employer.id
        response = self.client.get('/employer_dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Employer Dashboard', response.data)

if __name__ == '__main__':
    unittest.main()
