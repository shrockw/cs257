'''Tests for Flask application routes.'''
import unittest
from unittest.mock import MagicMock, patch
from app import app
from ProductionCode.datasource import DataSource

class TestFlaskRoutes(unittest.TestCase):
    '''Test case for Flask application routes.'''
    def setUp(self):
        self.app = app.test_client()
        #create a mock connection and cursor
        self.mock_conn = MagicMock()
        self.mock_cursor = self.mock_conn.cursor.return_value


    def test_homepage(self):
        '''Test the homepage route.'''
        response = self.app.get('/')
        self.assertIn(b"In the url after the /, \
        enter the word random, then a /, \
        then a number between 1 and 10. \
        This will return that many random recipes from the dataset. \
        For example: /random/3 will return 3 random recipes.", response.data, "Should match")

    @patch('ProductionCode.datasource.psycopg2.connect')
    def test_random_route(self, mock_connect):
        '''Test the random route.'''
        mock_connect.return_value = self.mock_conn
        self.mock_cursor.fetchall.return_value = "Fennel-Potato Soup with Smoked Salmon: Melt butter in heavy large pot over medium-high heat. Add fennel, leek, and fennel seeds and cook until vegetables begin to soften, stirring often, about 8 minutes. Add potatoes and 5 1/2 cups broth. Bring to boil; reduce heat to medium. Cover with lid slightly ajar and simmer until potatoes are tender, about 12 minutes. Working in batches, puree soup in blender. Return soup to pot and rewarm over medium heat, stirring often and thinning with more broth by 1/4 cupfuls for desired consistency. Season soup with salt and pepper. Divide soup among bowls. Garnish with smoked salmon and reserved chopped fennel fronds."
        data = DataSource()
        self.assertIn(
        "Fennel-Potato Soup",
        data.get_random_recipes(1), "Should match")

    def test_random_route_invalid(self):
        '''Test the random route with an invalid number.'''
        response = self.app.get('/random/11')
        self.assertIn(b"Please enter a number between 1 and 10.", response.data, "Should match")

    def test_search_include_route(self):
        '''Test the search include route.'''
        response = self.app.get('/search/include/cheese,broccoli')
        self.assertIn(
        b"Cavatappi with Broccolini, Brown Butter, and Sage",
        response.data, "Should match")

    def test_search_omit_route(self):
        '''Test the search omit route.'''
        response = self.app.get('/search/omit/cheese,broccoli')
        self.assertIn(
        b"Crispy Salt and Pepper Potatoes:",
        response.data, "Should match")

    def test_search_include_omit_route(self):
        '''Test the search include and omit route.'''
        response = self.app.get('/search/include/cheese,broccoli/omit/garlic')
        self.assertIn(
        b"Charred Steak and Broccolini with Cheese Sauce",
        response.data, "Should match")

    def test_invalid_input(self):
        '''Test the random recipes route with invalid input.'''
        response = self.app.get('/random/abc', follow_redirects=True)
        #self.assertEqual(response.status_code, 404)
        self.assertIn(b"Sorry, wrong format. Do this instead:",
                      response.data)

        response = self.app.get('/random/-1', follow_redirects=True)
        # self.assertEqual(response.status_code, 404)
        self.assertIn(b"Sorry, wrong format. Do this instead:",
                      response.data)
