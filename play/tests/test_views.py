from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

class IndexViewTestCase(TestCase):

    def test_returns_200(self):
        
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

class ResultsViewTestCase(TestCase):

    def test_returns_200(self):
        
        data = {
            'runs': 10,
            'user_hand': ['D14', 'D2'],
            'additional_players': 2,
            'additional_hands': [['', ''], ['H14', '']],
            'flop_cards': ['D3', 'D4', 'D5'],
            'turn_card': 'D13',
            'river_card': 'C14'
        }
               
        client = APIClient()
        response = client.post(reverse('results'), data, format='json')
        print(response)
        self.assertEqual(response.status_code, 200)
        
    def test_returns_error(self):
        
        data = {
            'whatever': 'whatever',
            'runs': 10
        }
        
        client = APIClient()
        response = client.post(reverse('results'), data, format='json')
        self.assertEqual(response.status_code, 200)