from django.test import TestCase
from play.models import Simulation
from play.serializers import SimulationSerializer

class SimulationSerializerTestCase(TestCase):
 
    def test_can_serialize_run_simulation_results(self):

        simulation = Simulation(
            runs=1000, 
            user_hand=[], 
            additional_players=2, 
            additional_hands=[['D14', 'C14']]
        )
        
        simulation.run_simulation()
            
        serializer = SimulationSerializer(simulation)
        print(serializer.data)
    
    
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
        
        self.assertTrue(['D14', 'C14'] == simulation.other_players[0].starting_hand or ['D14', 'C14'] == simulation.other_players[1].starting_hand)
        
        self.assertTrue(['H5', 'H6'] == simulation.other_players[0].starting_hand or ['H5', 'H6'] == simulation.other_players[1].starting_hand)
        
        self.assertEqual(len(simulation.all_players), 3)