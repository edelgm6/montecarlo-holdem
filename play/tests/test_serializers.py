from django.test import TestCase
from play.models import Game, Deck, Card, Stage, Suit, Hand
from play.serializers import SimulationSerializer
from play.handsorter import HandSorter

class SimulationSerializerTestCase(TestCase):
    
    def test_serializer_creates_simulation(self):

        data = {
            'runs': 1000,
            'user_hand': ['D2', 'D4'],
            'additional_players': 2,
            'additional_hands': [['D14', 'C14'], ['H5', 'H6']]   
        }


        serializer = SimulationSerializer(data=data)
        if serializer.is_valid():
            simulation = serializer.save()
            results = simulation.run_simulation()
            
        self.assertTrue(serializer.is_valid())
        
        self.assertEqual(simulation.runs, 1000)
        self.assertTrue(['D2', 'D4'] == simulation.user.starting_hand)
        
        self.assertTrue(['D14', 'C14'] == simulation.other_players[0].starting_hand or ['D14', 'C14'] == simulation.other_players[1].starting_hand)
        
        self.assertTrue(['H5', 'H6'] == simulation.other_players[0].starting_hand or ['H5', 'H6'] == simulation.other_players[1].starting_hand)