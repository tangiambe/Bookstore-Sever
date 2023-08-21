import unittest
from mongo_app import app

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_index(self):
        response = self.client.get('/index')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Bookstore', response.data)


    def test_register(self):
        response = self.client.post('/register', data={
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        }, follow_redirects=True)  

        self.assertEqual(response.status_code, 200)  
        self.assertIn(b'User Registration', response.data)  

    def test_login(self):
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login

    def test_search_books(self):
        response = self.client.get('/search_books')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Search Books', response.data)

    def test_search_results(self):
        response = self.client.get('/search_results')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Search Results', response.data)

    def test_create_book(self):
        # Log in first
        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testpassword'
        })
        response = self.client.post('/create_book', data={
            'title': 'Test Book',
            'author': 'Test Author',
            'category': '1',
            'id': '123456',
            'price': '19.99',
            'year': '2023',
            'quantity': '10'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Book created successfully!', response.data)

    def test_update_book(self):
        # Log in first
        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testpassword'
        })
        
        response = self.client.get('/update_book')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Update Book', response.data)

    def test_delete_book(self):
        # Log in first
        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testpassword'
        })
        
        response = self.client.get('/delete_book')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Delete Book', response.data)

if __name__ == '__main__':
    unittest.main()