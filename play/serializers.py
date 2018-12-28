from rest_framework import serializers
from play.models import Simulation
    
class SimulationSerializer(serializers.Serializer):
    runs = serializers.IntegerField(min_value=1)
    additional_players = serializers.IntegerField(max_value=7, min_value=1)
    