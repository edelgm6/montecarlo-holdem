from rest_framework import serializers
from play.models import Simulation
    
class SimulationSerializer(serializers.Serializer):
    runs = serializers.IntegerField(min_value=1)
    user_hand = serializers.ListField(
        child=serializers.CharField(max_length=3, min_length=2, allow_blank=True),
        min_length=0,
        max_length=2
    )
    
    additional_players = serializers.IntegerField(max_value=7, min_value=1)
    
    additional_hands = serializers.ListField(
        child=serializers.ListField(
            child=serializers.CharField(max_length=3, min_length=2, allow_blank=True),
            min_length=0, 
            max_length=1000)
    )
    
    results = serializers.DictField(
        child=serializers.DictField(
            child=serializers.IntegerField(min_value=0)
        ),
        read_only=True
    )
    
    wins = serializers.IntegerField(min_value=0, read_only=True)
    ties = serializers.IntegerField(min_value=0, read_only=True)
    losses = serializers.IntegerField(min_value=0, read_only=True)
    
    def create(self, validated_data):
        return Simulation(**validated_data)
    