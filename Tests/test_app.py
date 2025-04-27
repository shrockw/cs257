'''Tests for Flask application routes.'''
import unittest
import random
from app import app

class TestFlaskRoutes(unittest.TestCase):
    '''Test case for Flask application routes.'''
    def setUp(self):
        self.client = app.test_client()

    def test_homepage(self):
        '''Test the homepage route.'''
        response = self.client.get('/')
        self.assertIn(b"In the url after the /, \
        enter the word random, then a /, \
        then a number between 1 and 10. \
        This will return that many random recipes from the dataset. \
        For example: /random/3 will return 3 random recipes.", response.data)

    def test_random_route(self):
        '''Test the random route.'''
        random.seed(32719)
        response = self.client.get('/random/1')
        self.assertIn(
        b"Broccoli with Orecchiette: With food processor running, drop in garlic and finely chop.",
        response.data)

    def test_random_route_invalid(self):
        '''Test the random route with an invalid number.'''
        response = self.client.get('/random/11')
        self.assertIn(b"Please enter a number between 1 and 10.", response.data)

    def test_search_include_route(self):
        '''Test the search include route.'''
        response = self.client.get('/search/include/cheese,broccoli')
        self.assertIn(
        b"Recipes including ['cheese', 'broccoli']: <br><br>",
        response.data)

    def test_search_omit_route(self):
        '''Test the search omit route.'''
        response = self.client.get('/search/omit/cheese,broccoli')
        self.assertIn(
        b"Recipes omitting ['cheese', 'broccoli']: <br><br>",
        response.data)

    def test_search_include_omit_route(self):
        '''Test the search include and omit route.'''
        response = self.client.get('/search/include/cheese,broccoli/omit/garlic')
        self.assertIn(
        b"Recipes including ['cheese', 'broccoli'] and omitting ['garlic']: <br><br>",
        response.data)
