import unittest
from unittest.mock import MagicMock
from app import app, advanced_search, CV
from app import db
from unittest.mock import MagicMock, patch



class TestAdvancedSearch(unittest.TestCase):

    def setUp(self):
        self.filters = {
            'search_name': 'John Doe',
            'search_address': '',
            'search_experience': '',
            'search_skills': '',
            'search_contact_number': '',
            'search_past_experience': ''
        }

        self.cv1 = CV(id=1, candidate_id=1, full_name='John Doe', address='123 Elm St', experience=3,
                      skills='Python, Django', references='Jane Smith, Mike Johnson', contact_number='555-1234',
                      past_experience='Software Developer at XYZ Company')
        self.cv2 = CV(id=2, candidate_id=2, full_name='Jane Smith', address='456 Oak St', experience=5,
                      skills='Java, Spring', references='John Doe, Mike Johnson', contact_number='555-5678',
                      past_experience='Software Developer at ABC Company')

        db.session.query = MagicMock(return_value=db.session)
        db.session.filter = MagicMock(return_value=db.session)
        db.session.all = MagicMock(return_value=[self.cv1, self.cv2])

    @patch('app.CV.query')
    def test_advanced_search_by_name(self, mock_query):
        # Configure the mock_query object
        mock_query_instance = MagicMock()
        mock_query_instance.filter.return_value = mock_query_instance
        mock_query_instance.all.return_value = [self.cv1, self.cv2]
        mock_query.__get__ = MagicMock(return_value=mock_query_instance)

        with app.app_context():
            result = advanced_search(self.filters)
            self.assertEqual(len(result), 2)



if __name__ == '__main__':
    unittest.main()
