import os
import unittest

from app import app


class AnalyticsTestCase(unittest.TestCase):
    ############################
    #### setup and teardown ####
    ############################

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    def tearDown(self):
        pass

    def test_index(self):
        response = self.app.get('/analytics', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()