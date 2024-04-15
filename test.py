import unittest
import requests_mock
from app import app, get_data

class TestApp(unittest.TestCase):

    @requests_mock.Mocker()
    def test_get_data_success(self, mock_request):
        mock_request.get('https://jsonplaceholder.typicode.com/posts', json=[{'id': 1, 'title': 'Test Title', 'body': 'Test Body'}])
        data = get_data('posts')

        # Sprawdzenie czy funkcja zwraca poprawne dane
        self.assertEqual(data, [{'id': 1, 'title': 'Test Title', 'body': 'Test Body'}])

    @requests_mock.Mocker()
    def test_get_data_failure(self, mock_request):
        # Konfiguracja mocka dla zwracania statusu 404
        mock_request.get('https://jsonplaceholder.typicode.com/posts', status_code=404)
        data = get_data('posts')
        self.assertIsNone(data)

    def test_show_posts(self):
        with app.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)

    @requests_mock.Mocker()
    def test_search_posts(self, mock_request):
        
        mock_posts = [{'id': 1, 'title': 'Test Title 1', 'body': 'Test Body 1'}, 
                      {'id': 2, 'title': 'Test Title 2', 'body': 'Test Body 2'}]
        
        mock_request.get('https://jsonplaceholder.typicode.com/posts', json=mock_posts)
        
        with app.test_client() as client:
            # Test dla przypadku GET
            response = client.get('/')
            self.assertEqual(response.status_code, 200)

            # Test dla przypadku POST
            response = client.post('/', data={'min_chars': '5', 'max_chars': '120'})
            self.assertEqual(response.status_code, 200)

            # Test filtracji danych
            filtered_response = client.post('/', data={'min_chars': '5', 'max_chars': '120'})
            filtered_data = filtered_response.get_json()
            if filtered_data:
                self.assertEqual(len(filtered_data['posts']), 2)  
            else:
                self.fail("Filtered data is None")

            filtered_response = client.post('/', data={'min_chars': '10', 'max_chars': '120'})
            filtered_data = filtered_response.get_json()
            if filtered_data:
                self.assertEqual(len(filtered_data['posts']), 0)  
            else:
                self.fail("Filtered data is None")
            self.assertEqual(len(filtered_data['posts']), 0)  

if __name__ == '__main__':
    unittest.main()