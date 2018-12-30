from django.test import TestCase
from play.models import Simulation
from play.serializers import SimulationSerializer

class SimulationSerializerTestCase(TestCase):
 
    def test_successful_with_empty_cards(self):

        data = {
            'runs': 1000,
            'user_hand': ['D14', ''],
            'additional_players': 2,
            'additional_hands': [['', 'C14'], ['H14', '']]   
        }
        
            
        serializer = SimulationSerializer(data=data)
        valid = serializer.is_valid()
        simulation = serializer.save()
        print(simulation.user_hand)
        print(simulation.additional_hands)
        self.assertTrue(valid)
        self.assertEqual(simulation.user_hand, ['D14', ''])
        self.assertEqual(simulation.additional_hands, [['', 'C14'], ['H14', '']])

    def test_raises_error_if_duplicate_cards(self):

        data = {
            'runs': 1000,
            'user_hand': ['D14', 'H14'],
            'additional_players': 2,
            'additional_hands': [['D14', 'C14'], ['C14', 'D2']]   
        }
        
            
        serializer = SimulationSerializer(data=data)
        valid = serializer.is_valid()
        self.assertFalse(valid)

    def test_can_serialize_run_simulation_results(self):

        simulation = Simulation(
            runs=1000, 
            user_hand=[], 
            additional_players=2, 
            additional_hands=[['D14', 'C14']]
        )
        
        simulation.run_simulation()
            
        serializer = SimulationSerializer(simulation)
    
    
    def test_serializer_creates_simulation_with_single_starter_hand(self):

        data = {
            'runs': 1000,
            'user_hand': [],
            'additional_players': 2,
            'additional_hands': [['D14', 'C14']]   
        }

        serializer = SimulationSerializer(data=data)
        if serializer.is_valid():
            simulation = serializer.save()
            simulation.run_simulation()
            
        self.assertTrue(serializer.is_valid())
        
        self.assertEqual(simulation.runs, 1000)
        self.assertEqual(len(simulation.all_players), 3)

    def test_serializer_creates_simulation_without_starter_hands(self):

        data = {
            'runs': 1000,
            'user_hand': [],
            'additional_players': 2,
            'additional_hands': []   
        }


        serializer = SimulationSerializer(data=data)
        if serializer.is_valid():
            simulation = serializer.save()
            results = simulation.run_simulation()
            
        self.assertTrue(serializer.is_valid())
        
        self.assertEqual(simulation.runs, 1000)
        self.assertEqual(len(simulation.all_players), 3)

    def test_serializer_creates_simulation_with_starter_hands(self):

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
        
        self.assertTrue(['D14', 'C14'] == simulation.all_players[1].starting_hand or ['D14', 'C14'] == simulation.all_players[2].starting_hand)
        
        self.assertTrue(['H5', 'H6'] == simulation.all_players[1].starting_hand or ['H5', 'H6'] == simulation.all_players[2].starting_hand)
        
        self.assertEqual(len(simulation.all_players), 3)